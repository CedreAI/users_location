<sub>بسم الله الرحمن الرحیم</sub>
<br>
<h5>هدف: پیدا کردن لوکیشن کاربران و زمان ورود آنها به نرم افزار</h5>
<br>
<h6>مراحل اجرا:<br>
ابتدا با استفاده از ip-api.com لوکیشن کاربر رو از ip کاربر میگیریم و در فایل tsv ذخیره میکنیم.<br>
بعد با استفاده از لایبریری plotly اونها رو روی نقشه میزاریم.<br>
سپس با همون کتابخونه یک آمار کلی برای تعداد افراد وارد شده در زمان های مختلف را میسازیم.<br>
بعد از اون با استفاده از لایبریری dash یک slicer میسازیم که میتونیم بازه زمانی روزانه رو مشخص کنیم.<br>
بعد از مشخص کردن بازه زمانی دیتابیس آپدیت میشود و فقط کاربرانی که در آن روز ها وارد نرم افزار شده اند در دیتابیس میمانند و بقیه حذف میشوند.<br>
یک slicer ساعتی هم زیر نقشه میزاریم تا ساعت به ساعت کاربران رو روی نقشه نشان بدهد<h6>
<hr>
<h5>Objective: Find users' locations and when they enter the application</h5>
<br>
<h6>Execution steps:<br>
First, using ip-api.com, we get the user's location from the user ip and save it in a tsv file.<br>
Then we draw them on the map using plotly librarian.<br>
Then with the same library we make a general statistic for the number of people entered at different times.<br>
Then we use the dash library to create a slicer that you can specify daily.<br>
After specifying the time period, the database is updated and only the users who in those days the software entered in the database remain and the rest are deleted.<br>
We also place an hour slicer under the map to show users on the map hour by hour</h6>
