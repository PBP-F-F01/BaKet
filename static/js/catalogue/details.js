document.addEventListener("DOMContentLoaded", function () {
  const one = document.getElementById("first");
  const two = document.getElementById("second");
  const three = document.getElementById("third");
  const four = document.getElementById("fourth");
  const five = document.getElementById("fifth");

  const arr = [one, two, three, four, five];

  arr.forEach((element) => {
    element.addEventListener("mouseover", (event) => {
      console.log(event.target);
    });
  });
});
