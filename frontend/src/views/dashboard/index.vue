<template>
  <div class="page">
    <!-- 背景粒子 -->
    <canvas ref="particleCanvas" class="background-particles"></canvas>

    <!-- 主体内容 -->
    <div class="content">
      <!-- SVG 文字 -->
      <svg viewBox="0 0 800 100" class="neon-svg">
        <text x="50%" y="50%" dy=".3em" text-anchor="middle">主页太懒了不想写了</text>
      </svg>

      <!-- 动画人脸 -->
      <div class="face-container" ref="faceContainer">
        <svg viewBox="0 0 200 200" width="150" height="150" class="animated-face">
          <!-- 脸 -->
          <circle cx="100" cy="100" r="80" fill="#fdd" stroke="#ccc" stroke-width="2"/>
          <!-- 左眼 -->
          <circle cx="70" cy="70" r="10" fill="#fff"/>
          <circle :cx="eyeLeftX" cy="70" r="3" fill="#000"/>
          <!-- 右眼 -->
          <circle cx="130" cy="70" r="10" fill="#fff"/>
          <circle :cx="eyeRightX" cy="70" r="3" fill="#000"/>
          <!-- 嘴巴 -->
          <path :d="mouthPath" fill="none" stroke="#000" stroke-width="3" />
        </svg>
      </div>

      <!-- 提示按钮 -->
      <div class="floating-box">
        <p>别看了，真的没写内容 😎</p>
        <button class="glow-button" @click="shakeIt">点我试试？</button>
      </div>
    </div>

    <!-- 使用 v-html 注入 SVG 渐变定义，防止 Vite 报错 -->
    <div v-html="svgGradient" style="height: 0; width: 0; position: absolute;"></div>
  </div>
</template>

<script>
export default {
  name: "index",
  data() {
    return {
      mouseX: 0,
      mouseY: 0,
      faceX: 100, // 固定位置
      faceY: 100,
      maxDistance: 200, // 触发微笑的最大距离
      smileFactor: 0,   // 表情强度（0~1）
      svgGradient: `
        <svg>
          <defs>
            <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#ff00cc"/>
              <stop offset="50%" stop-color="#3333ff"/>
              <stop offset="100%" stop-color="#00ffcc"/>
            </linearGradient>
          </defs>
        </svg>
      `,
    };
  },
  computed: {
    eyeLeftX() {
      const dx = Math.max(-6, Math.min(6, this.mouseX - 70));
      return 70 + dx;
    },
    eyeRightX() {
      const dx = Math.max(-6, Math.min(6, this.mouseX - 130));
      return 130 + dx;
    },
    mouthPath() {
      const baseRadius = 40;
      const baseStart = Math.PI * 0.3;
      const baseEnd = Math.PI * 0.7;

      // 根据 smileFactor 弯曲嘴巴
      const curveOffset = this.smileFactor * Math.PI * 0.15;

      const startAngle = baseStart + curveOffset * 0.5;
      const endAngle = baseEnd - curveOffset * 0.5;

      const x1 = 100 + baseRadius * Math.cos(startAngle);
      const y1 = 100 + baseRadius * Math.sin(startAngle);
      const x2 = 100 + baseRadius * Math.cos(endAngle);
      const y2 = 100 + baseRadius * Math.sin(endAngle);

      return `M ${x1} ${y1} A ${baseRadius} ${baseRadius} 0 0 1 ${x2} ${y2}`;
    }
  },
  mounted() {
    window.addEventListener("mousemove", this.trackMouse);
    this.initParticles();
    requestAnimationFrame(this.animateSmile);
  },
  methods: {
    trackMouse(e) {
      const rect = this.$refs.faceContainer.getBoundingClientRect();
      this.mouseX = e.clientX - rect.left;
      this.mouseY = e.clientY - rect.top;
    },
    animateSmile() {
      // 计算鼠标到人脸中心的距离
      const dx = this.mouseX - 100;
      const dy = this.mouseY - 100;
      const distance = Math.sqrt(dx * dx + dy * dy);

      // 计算当前微笑系数（0~1）
      let targetSmile = Math.max(0, 1 - distance / this.maxDistance);

      // 平滑过渡
      this.smileFactor += (targetSmile - this.smileFactor) * 0.1;

      requestAnimationFrame(this.animateSmile);
    },
    initParticles() {
      const canvas = this.$refs.particleCanvas;
      const ctx = canvas.getContext("2d");

      let w, h;
      const setCanvasSize = () => {
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
      };
      setCanvasSize();
      window.addEventListener("resize", setCanvasSize);

      const particles = [];
      const total = 100;

      for (let i = 0; i < total; i++) {
        particles.push({
          x: Math.random() * w,
          y: Math.random() * h,
          vx: (Math.random() - 0.5) * 1,
          vy: (Math.random() - 0.5) * 1,
          radius: Math.random() * 2 + 1,
        });
      }

      const draw = () => {
        ctx.clearRect(0, 0, w, h);
        ctx.fillStyle = "#fff";
        ctx.strokeStyle = "rgba(255,255,255,0.2)";
        for (let p of particles) {
          p.x += p.vx;
          p.y += p.vy;
          if (p.x < 0 || p.x > w) p.vx *= -1;
          if (p.y < 0 || p.y > h) p.vy *= -1;

          ctx.beginPath();
          ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
          ctx.fill();

          for (let q of particles) {
            const dx = p.x - q.x;
            const dy = p.y - q.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < 100) {
              ctx.beginPath();
              ctx.moveTo(p.x, p.y);
              ctx.lineTo(q.x, q.y);
              ctx.stroke();
            }
          }
        }
        requestAnimationFrame(draw);
      };

      draw();
    },
    shakeIt() {
      alert("你摇到了一个空页面 🎲");
    }
  }
};
</script>

<style scoped>
.page {
  position: relative;
  min-height: 100vh;
  //background: radial-gradient(circle at top, #0f0f0f, #1a1a1a);
  overflow: hidden;
}

.background-particles {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 0;
  pointer-events: none;
}

.content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 40px;
  min-height: 100vh;
}

.neon-svg {
  font-size: 4rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-weight: bold;
  width: 100%;
  max-width: 800px;
}

.neon-svg text {
  fill: url(#gradient);
  text-shadow:
      0 0 5px #fff,
      0 0 10px #ff00cc,
      0 0 20px #3333ff,
      0 0 40px #00ffcc;
}

.face-container {
  margin-top: 40px;
  transition: transform 0.3s ease-out;
}

.animated-face {
  filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.5));
}

.floating-box {
  margin-top: 40px;
  padding: 20px 30px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 15px;
  backdrop-filter: blur(10px);
  text-align: center;
}

.glow-button {
  margin-top: 15px;
  padding: 10px 20px;
  font-size: 1rem;
  color: #fff;
  background: linear-gradient(45deg, #3333ff, #00ffcc);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow:
      0 0 10px #00ffcc,
      0 0 20px #3333ff;
}

.glow-button:hover {
  transform: scale(1.1);
  box-shadow:
      0 0 20px #ff00cc,
      0 0 30px #00ffcc,
      0 0 40px #3333ff;
}
</style>
