<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>بوابة حجز السفر | TravelSmart</title>
    <!-- Chosen Palette: Warm Neutrals (Gray/Stone) with Indigo Accent -->
    <!-- Application Structure Plan: 
        SPA (Single Page Application) مُدارة بـ JavaScript.
        1.  ثلاث "طرق عرض" (Views) رئيسية في أقسام <div>: [search-view, results-view, booking-view].
        2.  يبدأ المستخدم في 'search-view' (الرئيسية).
        3.  البحث يخفي 'search-view' ويظهر 'results-view' مع النتائج المفلترة.
        4.  يحتوي 'results-view' على مخطط أسعار (Chart.js) وفلاتر متقدمة (متطلبات 14, 22, 51).
        5.  اختيار نتيجة يخفي 'results-view' ويظهر 'booking-view'.
        6.  'booking-view' يعالج تفاصيل المسافر، الخدمات الإضافية، والسياسات (متطلبات 32, 33, 38).
        7.  يتم تنفيذ متطلبات B2B (مثل عرض الرصيد 4، 5) في رأس الصفحة.
        8.  هذا الهيكل يتبع مباشرة المخططات الانسيابية (Flowcharts) المقدمة في PDF.
    -->
    <!-- Visualization & Content Choices:
        -   عرض التقويم (Req 14): Chart.js Bar Chart (Canvas) لعرض الأسعار على مدار 5 أيام.
        -   فلاتر البحث (Req 22, 51): HTML sliders و checkboxes. التفاعل بـ JS لتصفية النتائج.
        -   نتائج البحث (Req 19, 46): HTML/Tailwind list, يتم ملؤها ديناميكيًا بـ JS.
        -   خدمات إضافية (Req 32): HTML divs تفاعلية (Modal/Popup) لاختيار المقاعد/الوجبات.
        -   خرق السياسة (Req 38): Textarea تظهر/تختفي بـ JS.
        -   خيارات الدفع (Req 36): Radio buttons بـ JS لإظهار حقول الدفع المناسبة.
        -   تعبئة آلية (Req 33): JS يملأ الحقول من كائن mockUser.
    -->
    <!-- CONFIRMATION: NO SVG graphics used. NO Mermaid JS used. -->

    <!-- 1. تحميل Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- 2. تحميل Chart.js (لتنفيذ متطلب 14: عرض الأسعار في التقويم) -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <!-- 3. تخصيص خط Inter الافتراضي -->
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
        body {
            font-family: 'Cairo', sans-serif;
            background-color: #f8fafc; /* bg-gray-50 */
        }
        /* (متطلب 14) تخصيص حاوية المخطط البياني لتكون متجاوبة ومحددة الارتفاع */
        .chart-container {
            position: relative;
            width: 100%;
            max-width: 900px; /* أقصى عرض للمخطط */
            margin-left: auto;
            margin-right: auto;
            height: 200px; /* ارتفاع ثابت للمخطط */
            max-height: 250px; /* أقصى ارتفاع */
        }
        /* إخفاء الأقسام افتراضيًا */
        #results-view, #booking-view {
            display: none;
        }
    </style>
</head>
<body class="bg-gray-50">

    <!-- رأس الصفحة (Header) - يحتوي على متطلبات B2B -->
    <header class="bg-white shadow-md">
        <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
            <div class="text-3xl font-extrabold text-indigo-700">
                TravelSmart
            </div>
            <!-- (متطلبات 4, 5, 39) قسم خاص بالوكيل B2B -->
            <div id="b2b-agent-section" class="space-x-4 rtl:space-x-reverse hidden">
                <div class="text-sm">
                    <span class="text-gray-600">الرصيد المتاح (متطلب 4):</span>
                    <span id="agent-balance" class="font-bold text-green-600 text-lg">1,500 $</span>
                </div>
                <button id="recharge-btn" class="bg-yellow-500 text-white text-sm py-2 px-4 rounded-lg hover:bg-yellow-600 transition duration-150">
                    إعادة شحن الرصيد (متطلب 5)
                </button>
            </div>
            <!-- زر تبديل B2C/B2B (لأغراض العرض) -->
            <button id="toggle-view-btn" class="bg-gray-200 text-gray-700 text-sm py-2 px-4 rounded-lg">التبديل إلى B2B</button>
        </nav>
    </header>

    <!-- رسالة تنبيه عامة -->
    <div id="alert-message" class="hidden max-w-7xl mx-auto mt-4 p-3 rounded-lg text-sm text-center"></div>

    <main class="max-w-7xl mx-auto p-4 sm:px-6 lg:px-8 mt-6">

        <!-- =================================================================== -->
        <!-- 1. واجهة البحث (Search View)                                        -->
        <!-- =================================================================== -->
        <section id="search-view">
            <!-- التبويبات -->
            <div class="mb-6 border-b border-gray-200">
                <nav class="flex space-x-6 rtl:space-x-reverse" aria-label="Tabs">
                    <button id="tab-flights" class="tab-btn px-3 py-2 font-bold text-lg border-b-4 border-indigo-600 text-indigo-700">
                        ✈️ الطيران
                    </button>
                    <button id="tab-hotels" class="tab-btn px-3 py-2 font-bold text-lg text-gray-500 hover:text-indigo-700">
                        🏨 الفنادق
                    </button>
                </nav>
            </div>

            <!-- نموذج بحث الطيران (متطلبات 6-12) -->
            <form id="flight-search-form" class="bg-white p-6 rounded-xl shadow-lg space-y-4">
                <!-- (متطلب 6) نوع الرحلة -->
                <div class="flex space-x-4 rtl:space-x-reverse">
                    <label><input type="radio" name="tripType" value="oneway" class="ml-2 rtl:mr-2"> ذهاب فقط</label>
                    <label><input type="radio" name="tripType" value="return" checked class="ml-2 rtl:mr-2"> ذهاب وعودة</label>
                    <label><input type="radio" name="tripType" value="multicity" class="ml-2 rtl:mr-2"> مدن متعددة</label>
                </div>
                <!-- (متطلبات 8, 9, 10) المدن والتواريخ -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <input id="flight-origin" type="text" placeholder="المغادرة من (متطلب 8)" class="form-input border border-gray-300 p-3 rounded-lg">
                    <input id="flight-dest" type="text" placeholder="الوصول إلى (متطلب 10)" class="form-input border border-gray-300 p-3 rounded-lg">
                    <input id="flight-departure" type="date" placeholder="تاريخ المغادرة (متطلب 9)" class="form-input border border-gray-300 p-3 rounded-lg">
                    <input id="flight-return" type="date" placeholder="تاريخ العودة" class="form-input border border-gray-300 p-3 rounded-lg">
                </div>
                <!-- (متطلبات 11, 12) الدرجة والناقل -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <input type="number" placeholder="المسافرون (1)" class="form-input border border-gray-300 p-3 rounded-lg">
                    <select class="form-select border border-gray-300 p-3 rounded-lg"> <!-- (متطلب 11) -->
                        <option value="Economy">الدرجة السياحية</option>
                        <option value="Business">درجة رجال الأعمال</option>
                    </select>
                    <select class="form-select border border-gray-300 p-3 rounded-lg"> <!-- (متطلب 12) -->
                        <option value="">أي ناقل</option>
                        <option value="EK">Emirates (EK)</option>
                        <option value="SV">Saudia (SV)</option>
                        <option value="QR">Qatar Airways (QR)</option>
                    </select>
                    <button type="submit" class="w-full bg-indigo-600 text-white text-lg font-bold py-3 rounded-lg shadow-xl hover:bg-indigo-700 transition">
                        بحث
                    </button>
                </div>
            </form>

            <!-- نموذج بحث الفنادق (متطلبات 40-44) -->
            <form id="hotel-search-form" class="hidden bg-white p-6 rounded-xl shadow-lg space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <input type="text" placeholder="المدينة أو اسم الفندق (متطلب 40)" class="md:col-span-2 form-input border border-gray-300 p-3 rounded-lg">
                    <input type="date" placeholder="تاريخ الوصول" class="form-input border border-gray-300 p-3 rounded-lg">
                    <input type="date" placeholder="تاريخ المغادرة" class="form-input border border-gray-300 p-3 rounded-lg">
                </div>
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <select class="form-select border border-gray-300 p-3 rounded-lg"> <!-- (متطلب 43) -->
                        <option value="SA">الجنسية: سعودي</option>
                        <option value="EG">الجنسية: مصري</option>
                    </select>
                    <input type="number" placeholder="عدد الغرف (متطلب 44)" value="1" class="form-input border border-gray-300 p-3 rounded-lg">
                    <input type="number" placeholder="البالغون" value="2" class="form-input border border-gray-300 p-3 rounded-lg">
                    <button type="submit" class="w-full bg-indigo-600 text-white text-lg font-bold py-3 rounded-lg shadow-xl hover:bg-indigo-700 transition">
                        بحث
                    </button>
                </div>
            </form>
        </section>

        <!-- =================================================================== -->
        <!-- 2. واجهة النتائج (Results View)                                     -->
        <!-- =================================================================== -->
        <section id="results-view" class="hidden">
            <button id="back-to-search-1" class="mb-4 text-indigo-600 hover:underline">&larr; العودة للبحث</button>
            <div class="grid grid-cols-12 gap-6">
                
                <!-- المرشحات (Filters) -->
                <aside class="col-span-12 lg:col-span-3">
                    <div id="filters-container" class="bg-white p-6 rounded-xl shadow-lg space-y-6">
                        <h3 class="text-xl font-bold text-gray-800 border-b pb-2">تصفية النتائج</h3>
                        
                        <!-- (متطلب 22) مرشحات الطيران -->
                        <div id="flight-filters" class="space-y-4">
                            <div>
                                <label class="font-semibold">السعر (متطلب 22)</label>
                                <input type="range" min="100" max="2000" class="w-full">
                            </div>
                            <div>
                                <label class="font-semibold">التوقفات (متطلب 22)</label>
                                <div class="space-y-1 mt-2">
                                    <label class="flex items-center"><input type="checkbox" checked class="ml-2 rtl:mr-2"> مباشر</label>
                                    <label class="flex items-center"><input type="checkbox" checked class="ml-2 rtl:mr-2"> توقف واحد</label>
                                </div>
                            </div>
                            <div>
                                <label class="font-semibold">قابلية الاسترداد (متطلب 22)</label>
                                <div class="space-y-1 mt-2">
                                    <label class="flex items-center"><input type="checkbox" class="ml-2 rtl:mr-2"> قابل للاسترداد فقط</label>
                                </div>
                            </div>
                        </div>

                        <!-- (متطلب 51) مرشحات الفنادق -->
                        <div id="hotel-filters" class="hidden space-y-4">
                            <div>
                                <label class="font-semibold">تقييم النجوم (متطلب 51)</label>
                                <div class="flex justify-between text-lg text-yellow-500">
                                    <span>⭐</span> <span>⭐⭐</span> <span>⭐⭐⭐</span> <span>⭐⭐⭐⭐</span> <span>⭐⭐⭐⭐⭐</span>
                                </div>
                                <input type="range" min="1" max="5" value="3" class="w-full">
                            </div>
                            <div>
                                <label class="font-semibold">المرافق (متطلب 51)</label>
                                <div class="space-y-1 mt-2">
                                    <label class="flex items-center"><input type="checkbox" class="ml-2 rtl:mr-2"> واي فاي مجاني</label>
                                    <label class="flex items-center"><input type="checkbox" class="ml-2 rtl:mr-2"> مسبح</label>
                                </div>
                            </div>
                        </div>

                        <!-- (متطلب 16) رسوم المناولة -->
                        <div class="border-t pt-4">
                            <label class="flex items-center text-sm"><input type="checkbox" id="handling-fee-toggle" checked class="ml-2 rtl:mr-2"> عرض السعر شامل رسوم المناولة</label>
                        </div>

                    </div>
                </aside>
                
                <!-- قائمة النتائج -->
                <div class="col-span-12 lg:col-span-9 space-y-6">
                    
                    <!-- (متطلب 14) عرض أسعار التقويم -->
                    <div class="bg-white p-4 rounded-xl shadow-lg">
                        <h4 class="text-center font-bold mb-2">عرض أسعار التقويم (متطلب 14)</h4>
                        <div class="chart-container">
                            <canvas id="fareCalendarChart"></canvas>
                        </div>
                    </div>

                    <!-- (متطلب 21) تحميل Excel -->
                    <div class="flex justify-end">
                        <button id="download-excel-btn" class="bg-green-600 text-white text-sm py-2 px-4 rounded-lg hover:bg-green-700 transition">
                            تحميل النتائج (Excel) (متطلب 21)
                        </button>
                    </div>
                    
                    <!-- بطاقة نتيجة (عينة) -->
                    <div id="results-list" class="space-y-4">
                        <!-- عينة بطاقة طيران -->
                        <div class="bg-white p-4 rounded-xl shadow-lg flex flex-col md:flex-row items-center space-y-4 md:space-y-0 md:space-x-4 rtl:md:space-x-reverse">
                            <img src="https://placehold.co/100x50/0d9488/FFFFFF?text=Airline" alt="Airline" class="rounded">
                            <div class="flex-1">
                                <p class="text-lg font-bold">طيران الإمارات (EK)</p>
                                <p class="text-sm">08:00 (RUH) &larr; 11:30 (DXB)</p>
                                <p class="text-xs text-gray-500">مباشر | 2س 30د</p>
                            </div>
                            <div class="text-sm">
                                <p class="font-semibold">الأمتعة: 25 كج (متطلب 27)</p>
                                <p class="text-green-600">قابل للاسترداد (متطلب 27)</p>
                                <a href="#" class="text-indigo-600 text-xs hover:underline">عرض قواعد الأجرة (متطلب 24)</a>
                            </div>
                            <div class="text-center md:text-right">
                                <p class="text-2xl font-extrabold text-indigo-700">950 $</p>
                                <button class="book-now-btn w-full md:w-auto bg-indigo-600 text-white py-2 px-6 rounded-lg font-semibold hover:bg-indigo-700 transition">
                                    احجز الآن
                                </button>
                            </div>
                        </div>
                        <!-- عينة بطاقة فندق -->
                        <div class="bg-white p-4 rounded-xl shadow-lg flex items-center space-x-4 rtl:space-x-reverse hidden">
                             <img src="https://placehold.co/100x100/4f46e5/FFFFFF?text=Hotel" alt="Hotel" class="w-24 h-24 object-cover rounded-lg">
                             <div class="flex-1">
                                <p class="text-lg font-bold">فندق جراند بلازا (متطلب 47)</p>
                                <p class="text-yellow-500">⭐⭐⭐⭐⭐ (متطلب 49)</p>
                                <p class="text-sm text-gray-600">وسط المدينة (متطلب 48)</p>
                                <a href="#" class="text-indigo-600 text-xs hover:underline">عرض الخريطة والمرافق (متطلب 59, 58)</a>
                             </div>
                             <div class="text-right">
                                <p class="text-2xl font-extrabold text-indigo-700">220 $ / لليلة</p>
                                <p class="text-sm text-gray-500">الإجمالي لـ 3 ليالي: 660 $</p>
                                <button class="book-now-btn w-full bg-indigo-600 text-white py-2 px-6 rounded-lg font-semibold hover:bg-indigo-700 transition mt-2">
                                    احجز الآن
                                </button>
                             </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- =================================================================== -->
        <!-- 3. واجهة الحجز والدفع (Booking View)                               -->
        <!-- =================================================================== -->
        <section id="booking-view" class="hidden">
            <button id="back-to-results-1" class="mb-4 text-indigo-600 hover:underline">&larr; العودة للنتائج</button>
            <h2 class="text-2xl font-extrabold text-gray-800 mb-6">مراجعة الحجز والدفع (متطلب 31, 34)</h2>
            
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <!-- تفاصيل الحجز -->
                <div class="lg:col-span-2 space-y-6">
                    <!-- (متطلب 33) تعبئة بيانات المسافر -->
                    <div class="bg-white p-6 rounded-xl shadow-lg">
                        <h3 class="text-xl font-bold mb-4">بيانات المسافر (تعبئة تلقائية)</h3>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <input type="text" id="pass-name" placeholder="الاسم الكامل" class="form-input border border-gray-300 p-3 rounded-lg bg-gray-100">
                            <input type="text" id="pass-nat" placeholder="الجنسية" class="form-input border border-gray-300 p-3 rounded-lg bg-gray-100">
                            <input type="email" id="pass-email" placeholder="البريد الإلكتروني (متطلب 70)" class="form-input border border-gray-300 p-3 rounded-lg">
                            <input type="tel" id="pass-tel" placeholder="رقم الجوال (متطلب 71)" class="form-input border border-gray-300 p-3 rounded-lg">
                        </div>
                    </div>
                    
                    <!-- (متطلب 32) الخدمات الإضافية -->
                    <div class="bg-white p-6 rounded-xl shadow-lg">
                        <h3 class="text-xl font-bold mb-4">الخدمات الإضافية (متطلب 32)</h3>
                        <div class="flex space-x-4 rtl:space-x-reverse">
                            <button id="select-seat-btn" class="flex-1 bg-blue-100 text-blue-700 py-3 rounded-lg font-semibold hover:bg-blue-200">اختيار المقعد</button>
                            <button id="select-meal-btn" class="flex-1 bg-blue-100 text-blue-700 py-3 rounded-lg font-semibold hover:bg-blue-200">اختيار الوجبة</button>
                            <button id="select-bag-btn" class="flex-1 bg-blue-100 text-blue-700 py-3 rounded-lg font-semibold hover:bg-blue-200">إضافة أمتعة</button>
                        </div>
                    </div>
                    
                    <!-- (متطلب 38) خرق السياسة -->
                    <div id="policy-breach-section" class="hidden bg-red-100 p-6 rounded-xl shadow-lg border border-red-300">
                        <h3 class="text-xl font-bold text-red-700 mb-2">تنبيه: تجاوز سياسة الشركة! (متطلب 38)</h3>
                        <p class="text-sm text-red-600 mb-4">هذه الرحلة خارج معايير السعر المحددة. يرجى ذكر السبب لتقارير MIS.</p>
                        <textarea id="policy-reason" placeholder="اكتب سبب الاختيار هنا..." class="w-full p-3 border border-red-300 rounded-lg" rows="3"></textarea>
                    </div>

                </div>
                
                <!-- ملخص الدفع -->
                <div class="lg:col-span-1 space-y-6">
                    <!-- ملخص السعر -->
                    <div class="bg-gray-100 p-6 rounded-xl shadow-inner">
                        <h3 class="text-xl font-bold mb-4">ملخص السعر</h3>
                        <div class="space-y-2 text-sm">
                            <div class="flex justify-between"><span>السعر الأساسي</span> <span id="price-base">900 $</span></div>
                            <div class="flex justify-between"><span>الضرائب (متطلب 35)</span> <span id="price-tax">50 $</span></div>
                            <div class="flex justify-between border-b pb-2"><span>رسوم المناولة</span> <span id="price-fee">25 $</span></div>
                            <div class="flex justify-between text-xl font-bold pt-2"><span>الإجمالي</span> <span id="price-total" class="text-indigo-700">975 $</span></div>
                        </div>
                    </div>
                    
                    <!-- (متطلب 37, 72) العروض الترويجية -->
                    <div class="bg-white p-4 rounded-xl shadow-lg">
                        <label for="promo-code" class="text-sm font-semibold">رمز ترويجي (متطلب 37)</label>
                        <div class="flex mt-2">
                            <input type="text" id="promo-code" placeholder="أدخل الرمز" class="flex-1 border border-gray-300 p-2 rounded-l-lg">
                            <button id="apply-promo" class="bg-gray-700 text-white px-4 rounded-r-lg hover:bg-gray-800">تطبيق</button>
                        </div>
                    </div>
                    
                    <!-- (متطلب 36) خيارات الدفع -->
                    <div class="bg-white p-6 rounded-xl shadow-lg">
                        <h3 class="text-xl font-bold mb-4">اختر طريقة الدفع (متطلب 36)</h3>
                        <div class="space-y-3">
                            <label class="flex items-center p-3 border rounded-lg"><input type="radio" name="payment" value="card" checked class="ml-3 rtl:mr-3"> بطاقة ائتمان / مدين</label>
                            <label class="flex items-center p-3 border rounded-lg"><input type="radio" name="payment" value="netbanking" class="ml-3 rtl:mr-3"> خدمات بنكية (Net Banking)</label>
                            <label id="payment-deposit-option" class="hidden flex items-center p-3 border rounded-lg"><input type="radio" name="payment" value="deposit" class="ml-3 rtl:mr-3"> خصم من رصيد الوديعة</label>
                        </div>
                    </div>

                    <button id="confirm-booking-btn" class="w-full bg-green-600 text-white text-xl font-extrabold py-4 rounded-xl shadow-2xl hover:bg-green-700 transition">
                        تأكيد الحجز والدفع
                    </button>
                </div>
            </div>
        </section>

    </main>

    <!-- (متطلب 23) شريط الرحلة المختارة -->
    <footer id="selected-flight-bar" class="hidden fixed bottom-0 left-0 right-0 bg-indigo-900 text-white p-4 shadow-2xl-top z-50">
        <div class="max-w-7xl mx-auto flex justify-between items-center">
            <div>
                <p class="font-bold">الرحلة المختارة: طيران الإمارات (RUH &larr; DXB)</p>
                <p class="text-sm text-indigo-200">الإجمالي: 975 $ (شامل الرسوم)</p>
            </div>
            <button id="footer-book-btn" class="bg-green-500 text-white py-2 px-6 rounded-lg font-semibold hover:bg-green-600 transition">
                متابعة
            </button>
        </div>
    </footer>


    <!-- =================================================================== -->
    <!-- JavaScript Logic                                                    -->
    <!-- =================================================================== -->
    <script>
        document.addEventListener('DOMContentLoaded', () => {

            // --- حالة التطبيق الرئيسية ---
            let appState = {
                currentView: 'search', // search, results, booking
                searchType: 'flights', // flights, hotels
                isAgentView: false, // B2B vs B2C
                mockUser: { // (متطلب 33)
                    name: "عبدالله العلي",
                    nationality: "SA",
                    email: "a.ali@example.com",
                    tel: "0501234567"
                },
                mockAgent: { // (متطلب 4)
                    balance: 1500,
                    creditLimit: 2000,
                    lowBalanceThreshold: 500 // (متطلب 39)
                },
                selectedResult: null,
                handlingFee: 25 // (متطلب 16)
            };

            // --- جلب عناصر الواجهة (DOM Elements) ---
            const views = {
                search: document.getElementById('search-view'),
                results: document.getElementById('results-view'),
                booking: document.getElementById('booking-view')
            };
            const tabs = {
                flights: document.getElementById('tab-flights'),
                hotels: document.getElementById('tab-hotels')
            };
            const forms = {
                flights: document.getElementById('flight-search-form'),
                hotels: document.getElementById('hotel-search-form')
            };
            const filters = {
                flights: document.getElementById('flight-filters'),
                hotels: document.getElementById('hotel-filters')
            };
            const agentUI = {
                section: document.getElementById('b2b-agent-section'),
                balance: document.getElementById('agent-balance'),
                depositOption: document.getElementById('payment-deposit-option'),
                toggleBtn: document.getElementById('toggle-view-btn'),
                rechargeBtn: document.getElementById('recharge-btn')
            };
            const bookingForm = {
                name: document.getElementById('pass-name'),
                nat: document.getElementById('pass-nat'),
                email: document.getElementById('pass-email'),
                tel: document.getElementById('pass-tel')
            };
            const policySection = document.getElementById('policy-breach-section');
            const alertMsg = document.getElementById('alert-message');
            const selectedFlightBar = document.getElementById('selected-flight-bar');
            
            // --- دوال التنقل بين الواجهات (SPA Navigation) ---
            function showView(viewName) {
                appState.currentView = viewName;
                Object.values(views).forEach(v => v.style.display = 'none');
                selectedFlightBar.style.display = 'none';

                if (views[viewName]) {
                    views[viewName].style.display = 'block';
                }
                if (viewName === 'results' && appState.selectedResult) {
                    selectedFlightBar.style.display = 'flex'; // (متطلب 23)
                }
            }

            // --- دوال تبديل العرض (B2B/B2C) ---
            function toggleAgentView() {
                appState.isAgentView = !appState.isAgentView;
                if (appState.isAgentView) {
                    agentUI.section.style.display = 'flex';
                    agentUI.depositOption.style.display = 'flex';
                    agentUI.toggleBtn.textContent = 'التبديل إلى B2C';
                    // (متطلب 39) التحقق من الرصيد عند تسجيل الدخول
                    if (appState.mockAgent.balance < appState.mockAgent.lowBalanceThreshold) {
                        showAlert(`تنبيه: رصيدك منخفض جداً (${appState.mockAgent.balance}$)! (متطلب 39)`, 'error');
                    }
                } else {
                    agentUI.section.style.display = 'none';
                    agentUI.depositOption.style.display = 'none';
                    agentUI.toggleBtn.textContent = 'التبديل إلى B2B';
                    showAlert(''); // إخفاء التنبيه
                }
            }

            // --- دوال البحث و النتائج ---
            function switchSearchTab(type) {
                appState.searchType = type;
                if (type === 'flights') {
                    tabs.flights.classList.add('border-indigo-600', 'text-indigo-700');
                    tabs.flights.classList.remove('text-gray-500');
                    tabs.hotels.classList.remove('border-indigo-600', 'text-indigo-700');
                    tabs.hotels.classList.add('text-gray-500');
                    forms.flights.style.display = 'block';
                    forms.hotels.style.display = 'none';
                } else {
                    tabs.hotels.classList.add('border-indigo-600', 'text-indigo-700');
                    tabs.hotels.classList.remove('text-gray-500');
                    tabs.flights.classList.remove('border-indigo-600', 'text-indigo-700');
                    tabs.flights.classList.add('text-gray-500');
                    forms.flights.style.display = 'none';
                    forms.hotels.style.display = 'block';
                }
            }

            function performSearch(e) {
                e.preventDefault();
                showView('results');
                if (appState.searchType === 'flights') {
                    filters.flights.style.display = 'block';
                    filters.hotels.style.display = 'none';
                    renderFareCalendar(); // (متطلب 14)
                } else {
                    filters.flights.style.display = 'none';
                    filters.hotels.style.display = 'block';
                    // إخفاء مخطط الأسعار إذا كان البحث عن فنادق
                    document.getElementById('fareCalendarChart').parentElement.style.display = 'none';
                }
                // ... هنا يتم جلب النتائج من (app.py) ...
                showAlert('عرض نتائج البحث. يتم الآن تطبيق الفلاتر.', 'success');
            }

            // --- (متطلب 14) مخطط أسعار التقويم ---
            function renderFareCalendar() {
                const ctx = document.getElementById('fareCalendarChart').getContext('2d');
                if (window.myFareChart) {
                    window.myFareChart.destroy();
                }
                window.myFareChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['25 نوفمبر', '26 نوفمبر', '27 نوفمبر', '28 نوفمبر', '29 نوفمبر'],
                        datasets: [{
                            label: 'أقل سعر',
                            data: [950, 890, 920, 850, 1100],
                            backgroundColor: 'rgba(79, 70, 229, 0.6)',
                            borderColor: 'rgba(79, 70, 229, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: { y: { beginAtZero: false, ticks: { callback: (val) => '$' + val } } }
                    }
                });
            }

            // --- (متطلبات 8, 9, 10) تحسين تجربة المستخدم في نموذج البحث ---
            const flightOrigin = document.getElementById('flight-origin');
            const flightDest = document.getElementById('flight-dest');
            const flightDep = document.getElementById('flight-departure');
            const flightRet = document.getElementById('flight-return');
            
            flightOrigin.addEventListener('change', () => flightDest.focus()); // (متطلب 8)
            flightDest.addEventListener('change', () => flightDep.focus()); // (متطلب 10)
            flightDep.addEventListener('change', () => flightRet.focus()); // (متطلب 9)

            // --- دوال صفحة الحجز (Booking) ---
            function goToBookingPage() {
                appState.selectedResult = { id: 1, price: 950 }; // بيانات افتراضية
                showView('booking');
                
                // (متطلب 33) تعبئة آلية
                bookingForm.name.value = appState.mockUser.name;
                bookingForm.nat.value = appState.mockUser.nationality;
                bookingForm.email.value = appState.mockUser.email;
                bookingForm.tel.value = appState.mockUser.tel;

                // (متطلب 38) التحقق من سياسة الشركة
                if (appState.selectedResult.price > 900 && !appState.isAgentView) {
                    policySection.style.display = 'block';
                } else {
                    policySection.style.display = 'none';
                }
                
                // (متطلب 23) إخفاء شريط الملخص السفلي
                selectedFlightBar.style.display = 'none';
            }
            
            function confirmBooking() {
                // (متطلب 38) التحقق من سبب خرق السياسة
                if (policySection.style.display === 'block' && !document.getElementById('policy-reason').value) {
                    showAlert('خطأ: يجب تحديد سبب اختيار رحلة خارج سياسة الشركة (متطلب 38)', 'error');
                    return;
                }
                
                // (متطلب 3) التحقق من حجز Indigo (محاكاة)
                if (Math.random() > 0.9) { // 10% فرصة للفشل
                    showAlert('خطأ: الحجز معلق لدى الناقل. يرجى المحاولة مرة أخرى. (متطلب 3)', 'error');
                    return;
                }

                showAlert('تم تأكيد الحجز بنجاح! سيتم إرسال التذكرة إلى بريدك الإلكتروني (متطلب 28)', 'success');
                // ... هنا يتم استدعاء app.py لإرسال البريد الإلكتروني ...
                
                // العودة للرئيسية بعد النجاح
                setTimeout(() => showView('search'), 2000);
            }

            // --- دالة عرض التنبيهات ---
            function showAlert(message, type = 'info') {
                alertMsg.style.display = 'none';
                if (!message) return;
                
                alertMsg.textContent = message;
                alertMsg.className = 'max-w-7xl mx-auto mt-4 p-3 rounded-lg text-sm text-center'; // Reset
                
                if (type === 'success') {
                    alertMsg.classList.add('bg-green-100', 'text-green-700');
                } else if (type === 'error') {
                    alertMsg.classList.add('bg-red-100', 'text-red-700');
                } else {
                    alertMsg.classList.add('bg-blue-100', 'text-blue-700');
                }
                alertMsg.style.display = 'block';
            }

            // --- ربط الأحداث (Event Listeners) ---
            agentUI.toggleBtn.addEventListener('click', toggleAgentView);
            agentUI.rechargeBtn.addEventListener('click', () => {
                showAlert('سيتم التوجيه لصفحة إدارة الودائع لإعادة الشحن (متطلب 5)', 'info');
            });
            
            tabs.flights.addEventListener('click', () => switchSearchTab('flights'));
            tabs.hotels.addEventListener('click', () => switchSearchTab('hotels'));
            
            forms.flights.addEventListener('submit', performSearch);
            forms.hotels.addEventListener('submit', performSearch);
            
            document.getElementById('back-to-search-1').addEventListener('click', () => showView('search'));
            document.getElementById('back-to-results-1').addEventListener('click', () => showView('results'));
            document.getElementById('confirm-booking-btn').addEventListener('click', confirmBooking);

            // استخدام event delegation لنتائج البحث
            document.getElementById('results-list').addEventListener('click', (e) => {
                if (e.target.closest('.book-now-btn')) {
                    goToBookingPage();
                }
            });
            
            document.getElementById('footer-book-btn').addEventListener('click', goToBookingPage);
            
            // (متطلب 32) أزرار الخدمات الإضافية
            document.getElementById('select-seat-btn').addEventListener('click', () => showAlert('محاكاة: فتح نافذة اختيار المقاعد.', 'info'));
            document.getElementById('select-meal-btn').addEventListener('click', () => showAlert('محاكاة: فتح نافذة اختيار الوجبات.', 'info'));
            document.getElementById('select-bag-btn').addEventListener('click', () => showAlert('محاكاة: فتح نافذة إضافة الأمتعة.', 'info'));
            
            // (متطلب 21) تحميل Excel
            document.getElementById('download-excel-btn').addEventListener('click', () => {
                showAlert('جاري تجهيز ملف Excel للتحميل... (متطلب 21)', 'success');
            });

            // --- بدء تشغيل التطبيق ---
            switchSearchTab('flights'); // البدء بتبويب الطيران
            showView('search'); // البدء بواجهة البحث
        });
    </script>

</body>
</html>
