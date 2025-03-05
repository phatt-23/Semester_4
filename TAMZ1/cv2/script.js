
function displayGreeting() 
{
    var name = document.getElementById('name').value;
    console.log("Name: \"" + name + "\"");
    if (name === "" || name === undefined) {
        window.alert('You did not fill in the name!')
    } else {
        const alrt = document.getElementById("greeter");
        alrt.message = "Hello " + name + "!";
        alrt.buttons = ['Dismiss'];
        alrt.present();
    }
}

var btn = document.getElementById("greet-alert");
console.log(btn);
btn.addEventListener('click', () => {
    console.log('clicked');
});

var datetime = document.getElementById("date-time");
console.log(datetime);

datetime.addEventListener('ionBlur', () => {
    console.log('ion blur event');
});

datetime.addEventListener('ionChange', () => {
    console.log(this);
});


//https://www.w3schools.com/jsref/jsref_obj_date.asp

// TODO 1: 
// upravit aby se zobrazovaly spravne dny jako ve video ukazce
// dulezite datumy si muzete upravit podle sebe, datum zubare, zkouskove obdobi, narozeniny atd.
// harmonogram semestru https://www.vsb.cz/cs/student/harmonogram/
// spravnost vysledku muzete overit zde: https://www.timeanddate.com/date/durationresult.html 

// TODO 2:
// vypocet kolik dnu zbyva ke zvolenemu datu

// TODO 3:
// pro zvoleny datum zobrazit odpovidajici znameni horoskopu
// odkaz na obrazky: http://mrl.cs.vsb.cz/data/vyuka/tamz/2024/02/img.zip
// HINT: 
// vyuzit muzete pomocne pole/promenne
// var namesZodiac = ["kozoroh", "vodnar","ryby","beran","byk","blizenci","rak","lev","panna","vahy","stir","strelec"]; 
// var breakDate = [21,20,21,21,21,22,23,24,23,23,23,22];
// var imagePath = namesZodiac[globalMonth] + ".png";

