<template>
  <div class="box">
    <div class="circle" :style="{ 'background-color': this.backgroundColor }">>
      <div v-for="i in numPoints" :key="i" class="points" :class="[i <= this.movieScore ? 'marked' : '']" :style="{ '--i': i + 1, '--bgColor': this.color, '--rot': getRotate() + 'deg'}"></div>
    </div>
    <div class="text">
      <h2>{{this.movieScore + this.suffix}}</h2>
    </div>
  </div>
</template>

<script>
export default {
  name: "ScoreCircle",
  props:["score", "bgColor"],
  data() {
    return {
      numPoints: 100,
      movieScore: this.score,
      color: "#3c3c3c",
      backgroundColor: "black",
      suffix: ""
    }
  },
  mounted() {
    this.validateScore()
    this.prepareRating()
    this.assignColor()
    this.backgroundColor = this.bgColor

  },
  methods: {
    getRotate() {
      return 360 / this.numPoints
    },
    assignColor() {
      if (this.movieScore >= 70) {
        this.color = '#0f0'
      } else if (this.movieScore >= 40) {
        this.color = "#f5c519"
      } else {
        this.color = "#ff0000"
      }
    },
    prepareRating() {
      let rating = this.movieScore
      this.movieScore = parseInt(parseInt(rating * 1000) / 100);
      if (this.movieScore < 10) {
        this.movieScore = "NR"
      } else {
        this.suffix = "%"
      }
    },
    validateScore() {
      this.movieScore = Math.max(this.movieScore, 0)
      this.movieScore = Math.min(this.movieScore, 100)
      
    }
  }
}
</script>
<style scoped>
.box
{
  position: relative;
  margin: 50px;
  z-index: -1;
}
.box .text
{
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%,-50%);
  text-align: center;
  color: #fff;
}
.box .text h2
{
  font-size: 64px;
  font-weight: 600;
  letter-spacing: 1px;
  border-radius: 3px;
}
.box .text
{
  font-size: 18px;
  display: block;
}

.circle
{
  width: 220px;
  height: 220px;
  display: flex;
  justify-content: center;
  align-items: center;
  /* background-color: #1f2020; */
  border-radius: 100%;
}
.circle .points
{
  width: 3px;
  height: 20px;
  background: #0007;
  position: absolute;
  border-radius: 3px;
  transform: rotate(calc(var(--i)*var(--rot))) translateY(-100px);
    
}
.points.marked
{
  animation: glow 0.04s linear forwards;
  animation-delay: calc(var(--i)*0.01s);
}

@keyframes glow
{
  0%
  {
    background: #0007;
    box-shadow: none;
  }
  100%
  {
    background: var(--bgColor);
    box-shadow: 0 0 10px var(--bgColor);
  }
}

</style>