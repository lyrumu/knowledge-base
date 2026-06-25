<!-- ---
title: "ABOUT ME"
kicker: "ABOUT ME · MODULE 04"
subtitle: "Some info about me"
description: ""
layout: "page"
showHero: true
showBreadcrumbs: true
showTableOfContents: true
--- --首页不想要这个东西了 因此注释掉>

<!-- ===== 头像 + 个人信息 + 联系方式 ===== -->
<div class="about-profile">
  <div class="about-profile-row">
    <img class="about-avatar" src="/image/melody.png" alt="lyrumu" />
    <div class="about-profile-text">
      <h2 class="about-name">lyrumu</h2>
      <p class="about-role">Student · Developer</p>
      <p class="about-location">Hangzhou, Zhejiang, China</p>
    </div>
  </div>

  <!-- iOS 风格毛玻璃联系方式 — 头像行下方一排图标 -->
  {{< about-contact >}}
</div>

## Technical stack
<!-- 基础类 .about-tag 默认蓝色（开发工具）；
     --purple / --green 两个修饰类按类别切换配色（语言框架 / AI & 前沿）。 -->
<div class="about-tags">
  <span class="about-tag">{{< icon "git" >}} Git</span>
  <span class="about-tag">{{< icon "linux" >}} Linux</span>
  <span class="about-tag">{{< icon "markdown" >}} Markdown</span>
  <span class="about-tag">{{< icon "python" >}} Python</span>
  <span class="about-tag about-tag--purple">{{< icon "hugo" >}} Hugo</span>
  <span class="about-tag about-tag--purple">{{< icon "cplusplus" >}} C++</span>
  <span class="about-tag about-tag--green">AI Agent</span>
  <span class="about-tag about-tag--green">{{< icon "flutter" >}} Flutter</span>
</div>

---

## GitHub Contribution

<img
  src="https://ghchart.rshah.org/lyrumu"
  alt="lyrumu's GitHub contribution chart"
  class="w-full my-4 rounded-lg"
/>

{{< site-stats >}}