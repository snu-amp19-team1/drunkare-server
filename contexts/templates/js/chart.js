/* Inference Result */
var results = [[3, 1, 1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 3], [5, 0, 0, 3, 7, 5, 0, 0, 2, 0, 0, 0, 0, 0, 6, 3]];

/* USER1 */
var ctx = document.getElementById('user1').getContext('2d');
var user_data1 = {
    labels: ['Touching Face', 'Pouring', 'Raising hand', 'Typing smartphone', 'Jotting', 'Clinking', 'Drink1',
             'Tissue', 'Drink2', 'Spoon', 'Chopstick', 'Photo', 'Fork', 'Stirring', 'Keyboard', 'Mouse'],
    datasets: [{
        label: 'My First dataset',
        backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850",
                          "#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#36a2eb","#ff6384"],
        borderColor: 'transparent',
        data: results[0]
    }]
}

var chart = new Chart(ctx, {
    type: 'pie',
    data: user_data1,
    options: {
        legend: {
          display: false
        },
        tooltips: {
          bodyFontSize: 30,
          bodyFontFamily: 'Karla'
        },
        responsive:true,
        maintainAspectRatio: false
    }
});


/* USER2 */
var ctx = document.getElementById('user2').getContext('2d');

var user_data2 = {
    labels: ['Touching Face', 'Pouring', 'Raising hand', 'Typing smartphone', 'Jotting', 'Clinking', 'Drink1',
             'Tissue', 'Drink2', 'Spoon', 'Chopstick', 'Photo', 'Fork', 'Stirring', 'Keyboard', 'Mouse'],
    datasets: [{
        label: 'My First dataset',
        backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850",
                          "#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#36a2eb","#ff6384"],
        borderColor: 'transparent',
        data: results[1]
    }]
}

var chart = new Chart(ctx, {
    type: 'pie',
    data: user_data2,
    options: {
        legend: {
          display: false
        },
        tooltips: {
          bodyFontSize: 30,
          bodyFontFamily: 'Karla'
        },
        responsive:true,
        maintainAspectRatio: false
    }
});
