"use strict";

window.addEventListener("DOMContentLoaded", () => {
    const tabs = document.querySelectorAll(".nav-item");
    const navs = document.querySelectorAll(".nav-link");
    const contentItems = document.querySelectorAll(".tab-pane");
    tabs.forEach((tab, index) => {
        tab.addEventListener("click", () => {
          contentItems.forEach(item => {
            item.classList.remove('active');
            item.classList.remove('show');
          })
          navs.forEach(item => {
            item.classList.remove('active');
          })
          navs[index].classList.add('active');
          contentItems[index].classList.add('show');
          contentItems[index].classList.add('active');
        });
      });
})