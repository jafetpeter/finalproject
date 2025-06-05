document.addEventListener("DOMContentLoaded", function () {
    const monthInput = document.getElementById("month");
    const form = document.getElementById("monthFilterForm");
  
    if (monthInput && form) {
      monthInput.addEventListener("change", function () {
        form.submit();
      });
    }
  });
  