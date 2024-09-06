

function roundDownByN(number, n) {
    return Math.floor(number / n) * n;
}

function roundDown20(number) {
    return Math.floor((number - 10) / 20) * 20 + 10;
}

function getDirection() {
    return document.getElementById('direction').value;
}

function getAltitudeDiff() {
    const alt = parseInt(document.getElementById('altitudeDiff').value);
    if (alt < -1000) {
        return "B";
    } else if (alt > 1000) {
        return "A";
    } else {
        return "L";
    }
}

function isShaded(val) {
    return val === "y" ? "Shaded" : "Unshaded";
}

function isSloped(val) {
    return val === "y" ? "Slope" : "NoSlope";
}

    
function roundToNearest(value, list) {
    return list.reduce((prev, curr) => {
        return (Math.abs(curr - value) < Math.abs(prev - value) ? curr : prev);
    });
}

function getConditions() {
    const conditions = {};
    conditions.dryBulbTemperature = roundDownByN(parseInt(document.getElementById('dryBulbTemperature').value), 10);
    if (conditions.dryBulbTemperature > 100) {
        conditions.dryBulbTemperature = 100
    } else if (conditions.dryBulbTemperature < 0) {
        conditions.dryBulbTemperature = 10;
    }
    conditions.relativeHumidityPercentage = roundDownByN(parseInt(document.getElementById('relativeHumidity').value), 5);
    conditions.direction = getDirection();
    conditions.slope = isSloped(document.getElementById('slope').value);
    conditions.shading = isShaded(document.getElementById('shading').value);

    const currentTime = new Date();
    const hourMin = currentTime.getHours() * 100 + currentTime.getMinutes();
    const timesOfDay = [800, 1000, 1200, 1400, 1600, 1800];
    
    conditions.timeOfDay = roundToNearest(hourMin, timesOfDay);

    conditions.altitudeDiff = getAltitudeDiff();
    return conditions;
}

async function fetchJson(file) {
    const response = await fetch(file);
    return await response.json();
}

async function fetchCsv(file) {
    const response = await fetch(file);
    const data = await response.text();
    const parsedData = {};
    const lines = data.split('\n');
    const header = lines[0].split(',');

    for (let i = 1; i < lines.length; i++) {
        const row = lines[i].split(',');
        if (row.length === header.length) {
            parsedData[row[0]] = {};
            for (let j = 1; j < header.length; j++) {
                parsedData[row[0]][header[j]] = row[j];
            }
        }
    }
    return parsedData;
}

async function getProperFireAdjustmentData() {
    const currentMonth = new Date().getMonth() + 1; // JavaScript months are 0-11
    if (5 <= currentMonth && currentMonth <= 7) {
        return await fetchJson('fire_table_b.json');
    } else if (currentMonth >= 11 || currentMonth === 1) {
        return await fetchJson('fire_table_d.json');
    } else {
        return await fetchJson('fire_table_c.json');
    }
}

function verifyValid() {
     // Get the form values
     const dryBulbTemperature = document.getElementById('dryBulbTemperature').value;
     const relativeHumidity = document.getElementById('relativeHumidity').value;
     const direction = document.getElementById('direction').value;
     const slope = document.getElementById('slope').value;
     const shading = document.getElementById('shading').value;
     const altitudeDiff = document.getElementById('altitudeDiff').value;
     
     // Clear error messages
     document.getElementById('errorMessage').style.display = 'none';
     document.getElementById('result').style.display = 'none';
     document.getElementById('saveButton').style.display = 'none';
     
     // Check if all fields are filled
     let isValid = true;
     const fields = [dryBulbTemperature, relativeHumidity, direction, slope, shading, altitudeDiff];
     const inputs = ['dryBulbTemperature', 'relativeHumidity', 'direction', 'slope', 'shading', 'altitudeDiff'];

     // Reset any previous errors
     inputs.forEach(input => document.getElementById(input).classList.remove('error'));

     fields.forEach((field, index) => {
         if (field === '') {
             document.getElementById(inputs[index]).classList.add('error');
             isValid = false;
         }
     });

     if (!isValid) {
         document.getElementById('errorMessage').innerText = 'Please fill out all fields correctly!';
         document.getElementById('errorMessage').style.display = 'block';
     }

     return isValid;
}

async function calculateProbability() {
    const isValid = verifyValid();
    if (!isValid) {
        return;
    }
    const conditions = getConditions();
    const initialTable = await fetchCsv('fire_table_a.csv');
    const adjustmentTable = await getProperFireAdjustmentData();
    const finalTable = await fetchJson('fire_table_e.json');

    const num = parseInt(initialTable[roundDown20(conditions.dryBulbTemperature).toString()][conditions.relativeHumidityPercentage.toString()]);
    let adjustmentNum;

    if (conditions.shading === "Shaded") {
        adjustmentNum = adjustmentTable[conditions.shading][conditions.direction][conditions.timeOfDay.toString()][conditions.altitudeDiff];
    } else {
        adjustmentNum = adjustmentTable[conditions.shading][conditions.direction][conditions.slope][conditions.timeOfDay.toString()][conditions.altitudeDiff];
    }

    const finalNum = num + parseInt(adjustmentNum);
    const probabilityOfIgnition = finalTable[conditions.shading][conditions.dryBulbTemperature.toString()][finalNum.toString()];

    const resultDiv = document.getElementById('result');
    resultDiv.style.display = 'block';
    resultDiv.textContent = `Probability of Ignition: ${probabilityOfIgnition}`;

    // Display the save button after calculation
    const saveButton = document.getElementById('saveButton');
    saveButton.style.display = 'inline-block';

    // Save configuration and result on button click
    saveButton.onclick = function () {
        saveConfiguration(conditions, probabilityOfIgnition);
    };
}

function saveConfiguration(conditions, probabilityOfIgnition) {
    const timestamp = new Date().toISOString();
    const savedData = {
        timestamp,
        conditions: {
            dryBulbTemperature: conditions.dryBulbTemperature,
            relativeHumidityPercentage: conditions.relativeHumidityPercentage,
            direction: conditions.direction,
            slope: conditions.slope,
            shading: conditions.shading,
            altitudeDiff: conditions.altitudeDiff,
            timeOfDay: conditions.timeOfDay
        },
        probabilityOfIgnition
    };

    // Retrieve saved configurations
    let savedConfigs = JSON.parse(localStorage.getItem('savedConfigs')) || [];

    // Add new configuration
    savedConfigs.push(savedData);

    // Save back to localStorage
    localStorage.setItem('savedConfigs', JSON.stringify(savedConfigs));

    alert('Configuration saved!');
    //displaySavedConfigurations(); // Update the list of saved configurations
}

function displaySavedConfigurations() {
    const savedConfigs = JSON.parse(localStorage.getItem('savedConfigs')) || [];
    const savedListDiv = document.getElementById('savedConfigsList');

    savedListDiv.innerHTML = ''; // Clear previous content

    savedConfigs.forEach(config => {
        const configElement = document.createElement('div');
        configElement.textContent = `
            Saved on ${new Date(config.timestamp).toLocaleString()} -
            Dry Bulb Temperature: ${config.conditions.dryBulbTemperature}, 
            Relative Humidity: ${config.conditions.relativeHumidityPercentage}, 
            Direction: ${config.conditions.direction}, 
            Slope: ${config.conditions.slope}, 
            Shading: ${config.conditions.shading}, 
            Altitude Diff: ${config.conditions.altitudeDiff}, 
            Time of Day: ${config.conditions.timeOfDay},
            Probability of Ignition: ${config.probabilityOfIgnition}
        `;
        savedListDiv.appendChild(configElement);
    });
}

