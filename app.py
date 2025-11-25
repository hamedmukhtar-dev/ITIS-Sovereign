<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Travel Booking Portal | TravelSmart</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
        body { font-family: 'Cairo', sans-serif; background-color: #f8fafc; }
        .chart-container { position: relative; width: 100%; max-width: 900px; margin-left: auto; margin-right: auto; height: 200px; max-height: 250px; }
        .hidden { display: none !important; }
        #results-view, #booking-view { display: none; }
    </style>
</head>
<body class="bg-gray-50">

    <!-- Header -->
    <header class="bg-white shadow-md">
        <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
            <div id="app-title" class="text-3xl font-extrabold text-indigo-700">TravelSmart</div>
            <div class="space-x-4 flex items-center">
                <select id="language-selector" class="py-2 px-3 border border-gray-300 rounded-lg text-sm bg-white">
                    <option value="ar">العربية (AR)</option>
                    <option value="en" selected>English (EN)</option>
                </select>
                <div id="b2b-agent-section" class="space-x-4 hidden">
                    <span class="text-sm"><span id="balance-label" class="text-gray-600">Balance:</span> <span id="agent-balance" class="font-bold text-green-600">1,500 $</span></span>
                    <button id="recharge-btn" class="bg-yellow-500 text-white text-sm py-2 px-4 rounded-lg">Recharge</button>
                </div>
                <button id="toggle-view-btn" class="bg-gray-200 text-gray-700 text-sm py-2 px-4 rounded-lg">Switch to B2B</button>
            </div>
        </nav>
    </header>

    <div id="alert-message" class="hidden max-w-7xl mx-auto mt-4 p-3 rounded-lg text-sm text-center"></div>

    <main class="max-w-7xl mx-auto p-4 sm:px-6 lg:px-8 mt-6">
        <!-- Search View -->
        <section id="search-view">
            <div class="mb-6 border-b border-gray-200">
                <nav class="flex space-x-6" aria-label="Tabs">
                    <button id="tab-flights" class="tab-btn px-3 py-2 font-bold text-lg border-b-4 border-indigo-600 text-indigo-700" data-key="flightsTab">✈️ Flights</button>
                    <button id="tab-hotels" class="tab-btn px-3 py-2 font-bold text-lg text-gray-500 hover:text-indigo-700" data-key="hotelsTab">🏨 Hotels</button>
                </nav>
            </div>

            <form id="flight-search-form" class="bg-white p-6 rounded-xl shadow-lg space-y-4">
                <div class="flex space-x-4">
                    <label><input type="radio" name="tripType" value="oneway" class="mr-2"><span data-key="oneWay"> One Way</span></label>
                    <label><input type="radio" name="tripType" value="return" checked class="mr-2"><span data-key="roundTrip"> Round Trip</span></label>
                    <label><input type="radio" name="tripType" value="multicity" class="mr-2"><span data-key="multiCity"> Multi-City</span></label>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <input id="flight-origin" type="text" placeholder="Origin" class="form-input border border-gray-300 p-3 rounded-lg" data-placeholder-key="originPlaceholder">
                    <input id="flight-dest" type="text" placeholder="Destination" class="form-input border border-gray-300 p-3 rounded-lg" data-placeholder-key="destinationPlaceholder">
                    <input id="flight-departure" type="date" placeholder="Departure Date" class="form-input border border-gray-300 p-3 rounded-lg" data-placeholder-key="departureDatePlaceholder">
                    <input id="flight-return" type="date" placeholder="Return Date" class="form-input border border-gray-300 p-3 rounded-lg" data-placeholder-key="returnDatePlaceholder">
                </div>
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <input type="number" placeholder="Passengers (1)" class="form-input border border-gray-300 p-3 rounded-lg" data-placeholder-key="passengersPlaceholder">
                    <select class="form-select border border-gray-300 p-3 rounded-lg"><option value="Economy" data-key="economyClass">Economy</option><option value="Business" data-key="businessClass">Business</option></select>
                    <select class="form-select border border-gray-300 p-3 rounded-lg"><option value="" data-key="anyCarrier">Any Carrier</option><option value="EK">Emirates (EK)</option></select>
                    <button type="submit" class="w-full bg-indigo-600 text-white text-lg font-bold py-3 rounded-lg shadow-xl hover:bg-indigo-700 transition" data-key="searchButton">Search</button>
                </div>
            </form>

            <form id="hotel-search-form" class="hidden bg-white p-6 rounded-xl shadow-lg space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <input type="text" placeholder="City or Hotel Name" class="md:col-span-2 form-input border border-gray-300 p-3 rounded-lg" data-placeholder-key="cityHotelPlaceholder">
                    <input type="date" placeholder="Check-in" class="form-input border border-gray-300 p-3 rounded-lg" data-placeholder-key="checkInPlaceholder">
                    <input type="date" placeholder="Check-out" class="form-input border border-gray-300 p-3 rounded-lg" data-placeholder-key="checkOutPlaceholder">
                </div>
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <select class="form-select border border-gray-300 p-3 rounded-lg"><option value="SA" data-key="nationalitySaudi">Nationality: Saudi</option></select>
                    <input type="number" placeholder="Rooms" value="1" class="form-input border border-gray-300 p-3 rounded-lg" data-placeholder-key="roomsPlaceholder">
                    <input type="number" placeholder="Adults" value="2" class="form-input border border-gray-300 p-3 rounded-lg" data-placeholder-key="adultsPlaceholder">
                    <button type="submit" class="w-full bg-indigo-600 text-white text-lg font-bold py-3 rounded-lg shadow-xl hover:bg-indigo-700 transition" data-key="searchButton">Search</button>
                </div>
            </form>
        </section>

        <!-- Results View -->
        <section id="results-view" class="hidden">
            <button id="back-to-search-1" class="mb-4 text-indigo-600 hover:underline" data-key="backToSearch">&larr; Back to Search</button>
            <div class="grid grid-cols-12 gap-6">
                <aside class="col-span-12 lg:col-span-3">
                    <div id="filters-container" class="bg-white p-6 rounded-xl shadow-lg space-y-6">
                        <h3 class="text-xl font-bold text-gray-800 border-b pb-2" data-key="filterResults">Filter Results</h3>
                        <div id="flight-filters" class="space-y-4">
                            <div><label class="font-semibold" data-key="priceFilter">Price</label><input type="range" min="100" max="2000" class="w-full"></div>
                            <div><label class="font-semibold" data-key="stopsFilter">Stops</label><div class="space-y-1 mt-2"><label class="flex items-center"><input type="checkbox" checked class="mr-2"><span data-key="directFlight"> Direct</span></label></div></div>
                        </div>
                        <div id="hotel-filters" class="hidden space-y-4">
                            <div><label class="font-semibold" data-key="starRatingFilter">Star Rating</label><input type="range" min="1" max="5" value="3" class="w-full"></div>
                        </div>
                        <div class="border-t pt-4"><label class="flex items-center text-sm"><input type="checkbox" id="handling-fee-toggle" checked class="mr-2"><span data-key="showFees"> Show Price Incl. Handling Fees</span></label></div>
                    </div>
                </aside>

                <div class="col-span-12 lg:col-span-9 space-y-6">
                    <div class="bg-white p-4 rounded-xl shadow-lg">
                        <h4 class="text-center font-bold mb-2" data-key="fareCalendar">Fare Calendar View</h4>
                        <div class="chart-container"><canvas id="fareCalendarChart"></canvas></div>
                    </div>
                    <div class="flex justify-end">
                        <button id="download-excel-btn" class="bg-green-600 text-white text-sm py-2 px-4 rounded-lg hover:bg-green-700 transition" data-key="downloadExcel">⬇️ Download Results (Excel)</button>
                    </div>
                    <div id="results-list" class="space-y-4">
                        <div class="bg-white p-4 rounded-xl shadow-lg flex flex-col md:flex-row items-center space-y-4 md:space-y-0 md:space-x-4">
                            <img src="https://placehold.co/100x50/0d9488/FFFFFF?text=Airline" alt="Airline" class="rounded">
                            <div class="flex-1">
                                <p class="text-lg font-bold">Emirates (EK)</p>
                                <p class="text-sm">08:00 (RUH) &larr; 11:30 (DXB)</p>
                                <p class="text-xs text-gray-500" data-key="directDuration">Direct | 2h 30m</p>
                            </div>
                            <div class="text-sm">
                                <p class="font-semibold" data-key="baggage">Baggage: 25 kg</p>
                                <p class="text-green-600" data-key="refundable">Refundable</p>
                                <a href="#" class="text-indigo-600 text-xs hover:underline" data-key="viewFareRules">View Fare Rules</a>
                            </div>
                            <div class="text-center md:text-right"><p class="text-2xl font-extrabold text-indigo-700">950 $</p><button class="book-now-btn w-full md:w-auto bg-indigo-600 text-white py-2 px-6 rounded-lg font-semibold hover:bg-indigo-700 transition" data-key="bookNow">Book Now</button></div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Booking View -->
        <section id="booking-view" class="hidden">
            <button id="back-to-results-1" class="mb-4 text-indigo-600 hover:underline" data-key="backToResults">&larr; Back to Results</button>
            <h2 class="text-2xl font-extrabold text-gray-800 mb-6" data-key="bookingReview">Booking Review and Payment</h2>
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div class="lg:col-span-2 space-y-6">
                    <div class="bg-white p-6 rounded-xl shadow-lg">
                        <h3 class="text-xl font-bold mb-4" data-key="travelerDetails">Traveler Details</h3>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <input type="text" id="pass-name" placeholder="Full Name" class="form-input border border-gray-300 p-3 rounded-lg bg-gray-100" data-placeholder-key="fullNamePlaceholder">
                            <input type="email" id="pass-email" placeholder="Email" class="form-input border border-gray-300 p-3 rounded-lg" data-placeholder-key="emailPlaceholder">
                        </div>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-lg">
                        <h3 class="text-xl font-bold mb-4" data-key="ancillaryServices">Ancillary Services</h3>
                        <div class="flex space-x-4">
                            <button id="select-seat-btn" class="flex-1 bg-blue-100 text-blue-700 py-3 rounded-lg font-semibold hover:bg-blue-200" data-key="selectSeat">Select Seat</button>
                            <button id="select-meal-btn" class="flex-1 bg-blue-100 text-blue-700 py-3 rounded-lg font-semibold hover:bg-blue-200" data-key="selectMeal">Select Meal</button>
                            <button id="select-bag-btn" class="flex-1 bg-blue-100 text-blue-700 py-3 rounded-lg font-semibold hover:bg-blue-200" data-key="addBaggage">Add Baggage</button>
                        </div>
                    </div>
                    <div id="policy-breach-section" class="hidden bg-red-100 p-6 rounded-xl shadow-lg border border-red-300">
                        <h3 class="text-xl font-bold text-red-700 mb-2" data-key="policyBreachTitle">Policy Breach Alert</h3>
                        <p class="text-sm text-red-700 mb-3">تجاوز سياسة الشركة: هناك حاجة لسبب قبل الموافقة.</p>
                        <div class="space-y-3">
                            <label class="text-sm font-semibold">اختر سبباً سريعاً</label>
                            <div class="flex space-x-2">
                                <button type="button" class="policy-template-btn px-3 py-2 bg-white border rounded" data-template="Business critical">Business critical</button>
                                <button type="button" class="policy-template-btn px-3 py-2 bg-white border rounded" data-template="Customer request">Customer request</button>
                                <button type="button" class="policy-template-btn px-3 py-2 bg-white border rounded" data-template="Price match">Price match</button>
                            </div>
                            <label class="text-sm font-semibold">أو اكتب السبب</label>
                            <textarea id="policy-reason" placeholder="Enter reason for out-of-policy selection..." class="w-full p-3 border border-red-300 rounded-lg" rows="3" data-placeholder-key="policyReasonPlaceholder"></textarea>
                        </div>
                    </div>
                </div>

                <div class="lg:col-span-1 space-y-6">
                    <div class="bg-gray-100 p-6 rounded-xl shadow-inner"><h3 class="text-xl font-bold mb-4" data-key="priceSummary">Price Summary</h3><div class="space-y-2 text-sm"><div class="flex justify-between"><span>Total</span> <span id="price-total" class="text-indigo-700">975 $</span></div></div></div>
                    <div class="bg-white p-4 rounded-xl shadow-lg"><label for="promo-code" class="text-sm font-semibold" data-key="promoCode">Promo Code</label><div class="flex mt-2"><input type="text" id="promo-code" class="flex-1 border border-gray-300 p-2 rounded-l-lg" data-placeholder-key="promoPlaceholder"><button id="apply-promo" class="bg-gray-700 text-white px-4 rounded-r-lg hover:bg-gray-800" data-key="applyButton">Apply</button></div></div>
                    <div class="bg-white p-6 rounded-xl shadow-lg"><h3 class="text-xl font-bold mb-4" data-key="choosePayment">Choose Payment Method</h3><div class="space-y-3"><label class="flex items-center p-3 border rounded-lg"><input type="radio" name="payment" value="card" checked class="mr-3"><span data-key="cardPayment"> Credit/Debit Card</span></label><label id="payment-deposit-option" class="hidden flex items-center p-3 border rounded-lg"><input type="radio" name="payment" value="deposit" class="mr-3"><span data-key="depositPayment"> Deposit Balance</span></label></div></div>
                    <button id="confirm-booking-btn" class="w-full bg-green-600 text-white text-xl font-extrabold py-4 rounded-xl shadow-2xl hover:bg-green-700 transition" data-key="confirmPayButton">Confirm Booking & Pay</button>
                </div>
            </div>
        </section>
    </main>

    <footer id="selected-flight-bar" class="hidden fixed bottom-0 left-0 right-0 bg-indigo-900 text-white p-4 shadow-2xl-top z-50">
        <div class="max-w-7xl mx-auto flex justify-between items-center"><p class="font-bold" id="selected-flight-text">Selected Flight: Emirates</p><button id="footer-book-btn" class="bg-green-500 text-white py-2 px-6 rounded-lg font-semibold" data-key="proceedButton">Proceed</button></div>
    </footer>

    <script>
        // Localization
        const L10N = {
            en: {
                appTitle: 'TravelSmart', flightsTab: '✈️ Flights', hotelsTab: '🏨 Hotels', oneWay: 'One Way', roundTrip: 'Round Trip', multiCity: 'Multi-City', searchButton: 'Search', backToSearch: 'Back to Search', filterResults: 'Filter Results', priceFilter: 'Price', stopsFilter: 'Stops', directFlight: 'Direct', showFees: 'Show Price Incl. Handling Fees', fareCalendar: 'Fare Calendar View', downloadExcel: '⬇️ Download Results (Excel)', bookNow: 'Book Now', backToResults: 'Back to Results', bookingReview: 'Booking Review and Payment', travelerDetails: 'Traveler Details', ancillaryServices: 'Ancillary Services', selectSeat: 'Select Seat', selectMeal: 'Select Meal', addBaggage: 'Add Baggage', policyBreachTitle: 'Policy Breach Alert', priceSummary: 'Price Summary', promoCode: 'Promo Code', applyButton: 'Apply', choosePayment: 'Choose Payment Method', cardPayment: 'Credit/Debit Card', depositPayment: 'Deposit Balance', confirmPayButton: 'Confirm Booking & Pay', balanceLabel: 'Balance:', toggleToB2B: 'Switch to B2B', toggleToB2C: 'Switch to B2C', rechargeBtn: 'Recharge', originPlaceholder: 'Origin', destinationPlaceholder: 'Destination', departureDatePlaceholder: 'Departure Date', returnDatePlaceholder: 'Return Date', passengersPlaceholder: 'Passengers (1)', economyClass: 'Economy', businessClass: 'Business', anyCarrier: 'Any Carrier', cityHotelPlaceholder: 'City or Hotel Name', checkInPlaceholder: 'Check-in', checkOutPlaceholder: 'Check-out', nationalitySaudi: 'Nationality: Saudi', roomsPlaceholder: 'Rooms', adultsPlaceholder: 'Adults', fullNamePlaceholder: 'Full Name', emailPlaceholder: 'Email', policyReasonPlaceholder: 'Enter reason for out-of-policy selection...', promoPlaceholder: 'Enter Promo Code...', policyReasonError: 'Error: Reason for out-of-policy selection is mandatory.', bookingPendingError: 'Error: Booking is pending with the carrier. Please try again.', bookingSuccess: 'Booking confirmed successfully! Ticket will be emailed.'
            },
            ar: {
                appTitle: 'ترافل سمارت', flightsTab: '✈️ الطيران', hotelsTab: '🏨 الفنادق', oneWay: 'ذهاب فقط', roundTrip: 'ذهاب وعودة', multiCity: 'مدن متعددة', searchButton: 'بحث', backToSearch: 'العودة للبحث', filterResults: 'تصفية النتائج', priceFilter: 'السعر', stopsFilter: 'التوقفات', directFlight: 'مباشر', showFees: 'عرض السعر شامل رسوم المناولة', fareCalendar: 'عرض أسعار التقويم', downloadExcel: '⬇️ تحميل النتائج (Excel)', bookNow: 'احجز الآن', backToResults: 'العودة للنتائج', bookingReview: 'مراجعة الحجز والدفع', travelerDetails: 'بيانات المسافر', ancillaryServices: 'الخدمات الإضافية', selectSeat: 'اختيار المقعد', selectMeal: 'اختيار الوجبة', addBaggage: 'إضافة أمتعة', policyBreachTitle: 'تنبيه: تجاوز سياسة الشركة', priceSummary: 'ملخص السعر', promoCode: 'رمز ترويجي', applyButton: 'تطبيق', choosePayment: 'اختر طريقة الدفع', cardPayment: 'بطاقة ائتمان / مدين', depositPayment: 'خصم من رصيد الوديعة', confirmPayButton: 'تأكيد الحجز والدفع', balanceLabel: 'الرصيد:', toggleToB2B: 'التبديل إلى B2B', toggleToB2C: 'التبديل إلى B2C', rechargeBtn: 'إعادة شحن', originPlaceholder: 'المغادرة من', destinationPlaceholder: 'الوصول إلى', departureDatePlaceholder: 'تاريخ المغادرة', returnDatePlaceholder: 'تاريخ العودة', passengersPlaceholder: 'المسافرون (1)', economyClass: 'الدرجة السياحية', businessClass: 'درجة رجال الأعمال', anyCarrier: 'أي ناقل', cityHotelPlaceholder: 'المدينة أو اسم الفندق', checkInPlaceholder: 'تاريخ الوصول', checkOutPlaceholder: 'تاريخ المغادرة', nationalitySaudi: 'الجنسية: سعودي', roomsPlaceholder: 'الغرف', adultsPlaceholder: 'البالغون', fullNamePlaceholder: 'الاسم الكامل', emailPlaceholder: 'البريد الإلكتروني', policyReasonPlaceholder: 'اكتب سبب الاختيار هنا...', promoPlaceholder: 'أدخل الرمز الترويجي...', policyReasonError: 'خطأ: يجب تحديد سبب اختيار رحلة خارج سياسة الشركة.', bookingPendingError: 'خطأ: الحجز معلق لدى الناقل. يرجى المحاولة مرة أخرى.', bookingSuccess: 'تم تأكيد الحجز بنجاح! سيتم إرسال التذكرة.'
            }
        };

        function t(key, lang) {
            if (!key) return '';
            if (!L10N[lang]) return key;
            return L10N[lang][key] || key;
        }

        document.addEventListener('DOMContentLoaded', function () {
            var appState = {
                currentView: 'search', searchType: 'flights', isAgentView: false, mockUser: { name: 'John Doe', email: 'john.doe@example.com' }, mockAgent: { balance: 1500, lowBalanceThreshold: 500 }, selectedResult: null, handlingFee: 25, currentLang: 'en'
            };

            var langSelector = document.getElementById('language-selector');
            var views = { search: document.getElementById('search-view'), results: document.getElementById('results-view'), booking: document.getElementById('booking-view') };
            var tabs = { flights: document.getElementById('tab-flights'), hotels: document.getElementById('tab-hotels') };
            var forms = { flights: document.getElementById('flight-search-form'), hotels: document.getElementById('hotel-search-form') };
            var filters = { flights: document.getElementById('flight-filters'), hotels: document.getElementById('hotel-filters') };
            var agentUI = { section: document.getElementById('b2b-agent-section'), depositOption: document.getElementById('payment-deposit-option'), toggleBtn: document.getElementById('toggle-view-btn') };
            var policySection = document.getElementById('policy-breach-section');
            var alertMsg = document.getElementById('alert-message');
            var selectedFlightBar = document.getElementById('selected-flight-bar');

            function showView(name) {
                appState.currentView = name;
                Object.keys(views).forEach(function (k) { if (views[k]) views[k].style.display = 'none'; });
                selectedFlightBar.style.display = 'none';
                if (views[name]) views[name].style.display = 'block';
            }

            function toggleAgentView() {
                appState.isAgentView = !appState.isAgentView;
                if (appState.isAgentView) {
                    agentUI.section.style.display = 'flex';
                    if (agentUI.depositOption) agentUI.depositOption.style.display = 'flex';
                    if (agentUI.toggleBtn) agentUI.toggleBtn.textContent = t('toggleToB2C', appState.currentLang);
                    if (appState.mockAgent.balance < appState.mockAgent.lowBalanceThreshold) showAlert('Alert: Low balance (' + appState.mockAgent.balance + '$)!', 'error');
                } else {
                    if (agentUI.section) agentUI.section.style.display = 'none';
                    if (agentUI.depositOption) agentUI.depositOption.style.display = 'none';
                    if (agentUI.toggleBtn) agentUI.toggleBtn.textContent = t('toggleToB2B', appState.currentLang);
                    showAlert('');
                }
            }

            function switchSearchTab(type) {
                appState.searchType = type;
                [tabs.flights, tabs.hotels].forEach(function (el) { if (el) el.classList.remove('border-indigo-600', 'text-indigo-700', 'text-gray-500'); });
                [forms.flights, forms.hotels].forEach(function (f) { if (f) f.style.display = 'none'; });
                if (type === 'flights') {
                    if (tabs.flights) tabs.flights.classList.add('border-indigo-600', 'text-indigo-700');
                    if (forms.flights) forms.flights.style.display = 'block';
                    if (tabs.hotels) tabs.hotels.classList.add('text-gray-500');
                    if (filters.flights) filters.flights.style.display = 'block';
                    if (filters.hotels) filters.hotels.style.display = 'none';
                } else {
                    if (tabs.hotels) tabs.hotels.classList.add('border-indigo-600', 'text-indigo-700');
                    if (forms.hotels) forms.hotels.style.display = 'block';
                    if (tabs.flights) tabs.flights.classList.add('text-gray-500');
                    if (filters.flights) filters.flights.style.display = 'none';
                    if (filters.hotels) filters.hotels.style.display = 'block';
                }
            }

            function performSearch(e) {
                if (e && e.preventDefault) e.preventDefault();
                showView('results');
                if (appState.searchType === 'flights') renderFareCalendar(appState.currentLang);
                showAlert('Displaying search results. Filters are being applied.', 'success');
            }

            function renderFareCalendar(lang) {
                var canvas = document.getElementById('fareCalendarChart');
                if (!canvas) return;
                var ctx = canvas.getContext('2d');
                if (window.myFareChart) window.myFareChart.destroy();
                var labels = (lang === 'ar') ? ['نوفمبر 25', 'نوفمبر 26', 'نوفمبر 27', 'نوفمبر 28', 'نوفمبر 29'] : ['Nov 25', 'Nov 26', 'Nov 27', 'Nov 28', 'Nov 29'];
                window.myFareChart = new Chart(ctx, { type: 'bar', data: { labels: labels, datasets: [{ label: t('priceFilter', lang), data: [950, 890, 920, 850, 1100], backgroundColor: 'rgba(79, 70, 229, 0.6)', borderWidth: 1 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: false, ticks: { callback: function (val) { return '$' + val; } } } } } });
            }

            function goToBookingPage() {
                appState.selectedResult = { id: 1, price: 950 };
                showView('booking');
                var userProfile = (appState.currentLang === 'ar') ? { name: 'عبدالله العلي', email: 'a.ali@example.com' } : appState.mockUser;
                var nameEl = document.getElementById('pass-name');
                var emailEl = document.getElementById('pass-email');
                if (nameEl) nameEl.value = userProfile.name || '';
                if (emailEl) emailEl.value = userProfile.email || '';
                if (appState.selectedResult.price > 900 && !appState.isAgentView) {
                    if (policySection) policySection.style.display = 'block';
                } else {
                    if (policySection) policySection.style.display = 'none';
                }
            }

            function confirmBooking() {
                var reasonEl = document.getElementById('policy-reason');
                if (policySection && policySection.style.display === 'block' && !appState.isAgentView) {
                    if (!reasonEl || !reasonEl.value.trim()) {
                        openPolicyModal();
                        return;
                    }
                }
                if (reasonEl) reasonEl.classList.remove('border-red-600','ring-2','ring-red-200');
                if (Math.random() > 0.9) { showAlert(t('bookingPendingError', appState.currentLang), 'error'); return; }
                showAlert(t('bookingSuccess', appState.currentLang), 'success');
                setTimeout(function () { showView('search'); }, 1200);
            }

            function showAlert(message, type) {
                if (!alertMsg) return;
                alertMsg.style.display = 'none';
                if (!message) return;
                alertMsg.textContent = message;
                alertMsg.className = 'max-w-7xl mx-auto mt-4 p-3 rounded-lg text-sm text-center';
                if (type === 'success') alertMsg.classList.add('bg-green-100', 'text-green-700');
                else if (type === 'error') alertMsg.classList.add('bg-red-100', 'text-red-700');
                else alertMsg.classList.add('bg-blue-100', 'text-blue-700');
                alertMsg.style.display = 'block';
            }

            // Language switcher
            langSelector.addEventListener('change', function (e) { appState.currentLang = e.target.value; translateUI(appState.currentLang, appState); });

            // events
            if (agentUI.toggleBtn) agentUI.toggleBtn.addEventListener('click', toggleAgentView);
            if (forms.flights) forms.flights.addEventListener('submit', performSearch);
            if (forms.hotels) forms.hotels.addEventListener('submit', performSearch);
            var backToSearch = document.getElementById('back-to-search-1'); if (backToSearch) backToSearch.addEventListener('click', function () { showView('search'); });
            var backToResults = document.getElementById('back-to-results-1'); if (backToResults) backToResults.addEventListener('click', function () { showView('results'); });
            var confirmBtn = document.getElementById('confirm-booking-btn'); if (confirmBtn) confirmBtn.addEventListener('click', confirmBooking);
            var resultsList = document.getElementById('results-list'); if (resultsList) resultsList.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('.book-now-btn')) goToBookingPage(); });
            var footerBook = document.getElementById('footer-book-btn'); if (footerBook) footerBook.addEventListener('click', goToBookingPage);

            var downloadBtn = document.getElementById('download-excel-btn'); if (downloadBtn) downloadBtn.addEventListener('click', function () {
                var rows = [['Airline','From','To','Depart','Arrive','Price'], ['Emirates','RUH','DXB','08:00','11:30','950']];
                var csv = rows.map(function (r) { return r.map(function (c) { return '"' + String(c).replace(/"/g,'""') + '"'; }).join(','); }).join('\n');
                var blob = new Blob([csv], { type: 'text/csv' }); var url = URL.createObjectURL(blob); var a = document.createElement('a'); a.href = url; a.download = 'results.csv'; document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
            });

            // quick UX
            var flightOrigin = document.getElementById('flight-origin'); var flightDest = document.getElementById('flight-dest'); var flightDep = document.getElementById('flight-departure'); var flightRet = document.getElementById('flight-return');
            if (flightOrigin) flightOrigin.addEventListener('change', function () { if (flightDest) flightDest.focus(); });
            if (flightDest) flightDest.addEventListener('change', function () { if (flightDep) flightDep.focus(); });
            if (flightDep) flightDep.addEventListener('change', function () { if (flightRet) flightRet.focus(); });
            if (tabs.flights) tabs.flights.addEventListener('click', function () { switchSearchTab('flights'); });
            if (tabs.hotels) tabs.hotels.addEventListener('click', function () { switchSearchTab('hotels'); });

            // Build a modal using DOM methods to avoid template literal pitfalls
            var policyModal = document.createElement('div');
            policyModal.id = 'policy-modal';
            policyModal.className = 'hidden fixed inset-0 bg-black/40 flex items-center justify-center z-50';
            var modalInner = document.createElement('div');
            modalInner.className = 'bg-white rounded-xl shadow-xl max-w-xl w-full p-6';
            modalInner.innerHTML = '<h3 class="text-lg font-bold mb-3">Reason for Out-of-Policy Selection</h3>' +
                '<p class="text-sm text-gray-600 mb-3">Please provide a short reason before confirming this booking.</p>' +
                '<div class="space-y-3">' +
                '<label class="text-sm font-semibold">Quick templates</label>' +
                '<div class="flex gap-2">' +
                '<button type="button" class="policy-modal-template px-3 py-2 border rounded">Business critical</button>' +
                '<button type="button" class="policy-modal-template px-3 py-2 border rounded">Customer request</button>' +
                '<button type="button" class="policy-modal-template px-3 py-2 border rounded">Price match</button>' +
                '</div>' +
                '<textarea id="policy-modal-text" class="w-full p-3 border rounded" rows="4" placeholder="Enter reason..."></textarea>' +
                '</div>' +
                '<div class="mt-4 flex justify-end gap-3">' +
                '<button id="policy-modal-cancel" class="px-4 py-2 rounded border">Cancel</button>' +
                '<button id="policy-modal-submit" class="px-4 py-2 rounded bg-indigo-600 text-white">Submit Reason</button>' +
                '</div>';
            policyModal.appendChild(modalInner);
            document.body.appendChild(policyModal);

            var policyModalText = document.getElementById('policy-modal-text');
            var policyModalSubmit = document.getElementById('policy-modal-submit');
            var policyModalCancel = document.getElementById('policy-modal-cancel');

            document.addEventListener('click', function (e) {
                if (!e.target) return;
                if (e.target.matches && e.target.matches('.policy-template-btn')) {
                    var val = e.target.getAttribute('data-template');
                    var reasonInline = document.getElementById('policy-reason'); if (reasonInline) reasonInline.value = val;
                }
                if (e.target.matches && e.target.matches('.policy-modal-template')) {
                    if (policyModalText) policyModalText.value = e.target.textContent.trim();
                }
            });

            function openPolicyModal() { if (policyModal) { policyModal.classList.remove('hidden'); if (policyModalText) { policyModalText.value = ''; policyModalText.focus(); } } }
            function closePolicyModal() { if (policyModal) policyModal.classList.add('hidden'); }

            if (policyModalCancel) policyModalCancel.addEventListener('click', function () { closePolicyModal(); var reasonInline = document.getElementById('policy-reason'); if (reasonInline) { reasonInline.classList.add('border-red-600','ring-2','ring-red-200'); reasonInline.focus(); } });

            if (policyModalSubmit) policyModalSubmit.addEventListener('click', function () {
                var userText = policyModalText ? policyModalText.value.trim() : '';
                if (!userText) { if (policyModalText) { policyModalText.classList.add('border-red-600'); policyModalText.focus(); } return; }
                var reasonInline = document.getElementById('policy-reason'); if (reasonInline) reasonInline.value = userText;
                closePolicyModal();
                // proceed
                confirmBooking();
            });

            // init UI translation and view
            appState.currentLang = langSelector.value;
            translateUI(appState.currentLang, appState);
            switchSearchTab('flights');
            showView('search');

            // exposed small helpers
            window._travelApp = { appState: appState, goToBookingPage: goToBookingPage };
        });

        // translateUI defined after DOMContent to keep file organized
        function translateUI(lang, appState) {
            var isAR = lang === 'ar';
            document.documentElement.dir = isAR ? 'rtl' : 'ltr';
            document.documentElement.lang = lang;
            document.querySelectorAll('[data-key]').forEach(function (el) { var key = el.getAttribute('data-key'); if (key) el.textContent = t(key, lang); });
            document.querySelectorAll('[data-placeholder-key]').forEach(function (el) { var key = el.getAttribute('data-placeholder-key'); if (key) el.placeholder = t(key, lang); });
            var titleEl = document.getElementById('app-title'); if (titleEl) titleEl.textContent = t('appTitle', lang);
            var balanceLabel = document.getElementById('balance-label'); if (balanceLabel) balanceLabel.textContent = t('balanceLabel', lang);
            var selectedFlightText = document.getElementById('selected-flight-text'); if (selectedFlightText) selectedFlightText.textContent = isAR ? 'الرحلة المختارة: طيران الإمارات' : 'Selected Flight: Emirates';
            var toggleBtn = document.getElementById('toggle-view-btn'); if (toggleBtn && appState) toggleBtn.textContent = appState.isAgentView ? t('toggleToB2C', lang) : t('toggleToB2B', lang);
        }
    </script>
</body>
</html>
