<template>
  <div id="app">
    <menubar />
    <router-view class="main-content"></router-view>
    <factrank-footer />
  </div>
</template>

<script>
import MenuBar from "@/components/MenuBar";
import Footer from "@/components/Footer";

export default {
  name: "app",
  components: {
    menubar: MenuBar,
    "factrank-footer": Footer,
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Raleway:ital,wght@1,900&display=swap");

th,
td {
  font-weight: inherit;
}

.navbar-brand,
.h1,
h1,
.h2,
h2,
.h3,
h3,
.h4,
h4 {
  font-family: "Raleway", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji",
    "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
  font-weight: 700 !important;
  font-style: italic !important;
}

.container h3,
.container h2 {
  margin: 2.5rem 0rem;
  color: #1976d2;
}
.bg-primary-color h3,
.bg-primary-color h2 {
  color: #ffffff !important;
}
.bg-primary-color > .container > div > .table {
  color: #ffffff !important;
}
.bg-primary-color
  > .container
  > div
  > .table
  > tbody
  > tr
  > td
  > blockquote
  > footer.blockquote-footer {
  color: #ffffff !important;
}
.bg-primary-color
  > .container
  > div
  > .table
  > tbody
  > tr
  > td
  > blockquote
  > footer.blockquote-footer
  > p
  > a.text-secondary {
  color: #ffffff !important;
}
.bg-primary-color
  > .container
  > div
  > .table
  > tbody
  > tr
  > td
  > blockquote
  > footer.blockquote-footer
  > p
  > a.text-secondary
  > svg.twitter {
  color: #ffffff !important;
}
.bg-primary-color
  > .container
  > div
  > .table
  > tbody
  > tr
  > td
  > blockquote
  > p
  > span.text-context {
  color: #63a4ff !important;
}
.bg-primary-color
  > .container
  > div
  > .table
  > tbody
  > tr
  > td
  > blockquote
  > span
  > .feedback-results
  > button {
  color: #ffffff !important;
  border-color: #ffffff !important;
}
.bg-primary-color
  > .container
  > div
  > .table
  > tbody
  > tr
  > td
  > blockquote
  > span
  > .text-secondary {
  color: #ffffff !important;
}

.main-content a {
  color: #1976d2;
  text-decoration: underline;
}

html {
  height: 100%;
}
body {
  min-height: 100%;
  padding: 0;
  margin: 0;
  position: relative;
}

body::after {
  content: "";
  display: block;
  height: 140px;
}

footer.footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 140px;
}
.primary-color {
  color: #1976d2;
}
.secondary-color {
  color: #ffffff !important;
}
.bg-primary-color {
  background-color: #1976d2 !important;
}
.bg-tertiary-color {
  background-color: #f5f5f5 !important;
}
.main-content {
  margin-top: 2rem;
}
.spacing {
  height: 3rem;
}
</style>
