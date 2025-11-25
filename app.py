import React, { useState, useEffect } from 'react';
import { getAuth } from 'firebase/auth';
import { initializeApp } from 'firebase/app';

// ====================================================================
// 1. ملف JSON للترجمة (Localization Data)
// ====================================================================
const translations = {
    AR: {
        title: "مراجعة الحجز النهائي",
        subtitle: "ملخص الحجز وتفاصيل الدفع",
        logoutAlert: "⚠️ تنبيه (B2B): رصيدك الحالي (%1$) منخفض جداً. يرجى إعادة الشحن.",
        sectionFlight: "تفاصيل رحلة الطيران",
        carrier: "الناقل",
        route: "المسار",
        departureDate: "تاريخ المغادرة",
        fareBasis: "قاعدة الأجرة",
        ancillaries: "المقعد/الوجبة",
        selectAncillaries: "اختيار المقعد والوجبة",
        sectionHotel: "تفاصيل الإقامة",
        hotelName: "اسم الفندق",
        location: "الموقع",
        rating: "التصنيف",
        roomType: "الغرفة",
        cancellation: "سياسة الإلغاء",
        viewMap: "عرض المرافق والخريطة",
        sectionTraveler: "بيانات المسافر (تعبئة تلقائية)",
        fullName: "الاسم الكامل",
        nationality: "الجنسية",
        email: "البريد الإلكتروني",
        mobile: "رقم الجوال",
        policyBreachTitle: "تنبيه: تجاوز سياسة الشركة!",
        policyBreachText: "هذه الرحلة خارج معايير السعر المحددة. يجب تقديم سبب.",
        policyReasonPlaceholder: "يرجى كتابة سبب اختيار هذه الرحلة...",
        summaryTitle: "ملخص السعر (%1$)",
        basePrice: "السعر الأساسي",
        taxes: "الضرائب والرسوم",
        markup: "رسوم الربح (Markup)",
        finalTotal: "الإجمالي النهائي",
        promoTitle: "تطبيق رمز ترويجي",
        promoPlaceholder: "أدخل الرمز الترويجي...",
        apply: "تطبيق",
        paymentMethod: "طريقة الدفع",
        confirmPayment: "تأكيد الدفع والإرسال",
        deposit: "الوديعة",
        creditCard: "بطاقة ائتمانية",
        debitCard: "بطاقة مدين",
        netBanking: "الخدمات المصرفية عبر الإنترنت",
        errorInvalidPromo: "خطأ: رمز ترويجي غير صالح.",
        errorPolicyReason: "خطأ: يرجى تحديد سبب اختيار رحلة خارج سياسة الشركة.",
        errorInsufficientBalance: "خطأ: رصيدك غير كافٍ لإتمام الحجز! يرجى إعادة الشحن (%1$).",
        successBooking: "✅ جاري إرسال الحجز (PNR) عبر %1$. سيتم إرسال التذكرة بالبريد الإلكتروني.",
    },
    EN: {
        title: "Final Booking Review",
        subtitle: "Booking Summary and Payment Details",
        logoutAlert: "⚠️ Alert (B2B): Your current balance (%1$) is too low. Please recharge.",
        sectionFlight: "Flight Details",
        carrier: "Carrier",
        route: "Route",
        departureDate: "Departure Date",
        fareBasis: "Fare Basis",
        ancillaries: "Seat/Meal",
        selectAncillaries: "Select Seat & Meal",
        sectionHotel: "Accommodation Details",
        hotelName: "Hotel Name",
        location: "Location",
        rating: "Rating",
        roomType: "Room Type",
        cancellation: "Cancellation Policy",
        viewMap: "View Facilities & Map",
        sectionTraveler: "Traveler Information (Auto-filled)",
        fullName: "Full Name",
        nationality: "Nationality",
        email: "Email Address",
        mobile: "Mobile Number",
        policyBreachTitle: "Alert: Policy Breach!",
        policyBreachText: "This flight is outside defined fare standards. A reason must be provided.",
        policyReasonPlaceholder: "Please type the reason for choosing this flight...",
        summaryTitle: "Price Summary (%1$)",
        basePrice: "Base Price",
        taxes: "Taxes & Fees",
        markup: "Markup Fee",
        finalTotal: "Final Total",
        promoTitle: "Apply Promo Code",
        promoPlaceholder: "Enter Promo Code...",
        apply: "Apply",
        paymentMethod: "Payment Method",
        confirmPayment: "Confirm Payment & Submit",
        deposit: "Deposit",
        creditCard: "Credit Card",
        debitCard: "Debit Card",
        netBanking: "Net Banking",
        errorInvalidPromo: "Error: Invalid promo code.",
        errorPolicyReason: "Error: Please specify a reason for choosing an out-of-policy flight.",
        errorInsufficientBalance: "Error: Insufficient balance to complete booking! Please recharge (%1$).",
        successBooking: "✅ Booking (PNR) processing via %1$. Ticket will be emailed.",
    }
};

// دالة جلب النص بناءً على اللغة
const useTranslation = (language) => {
    const t = (key, ...args) => {
        let text = translations[language][key] || key;
        args.forEach((arg, index) => {
            text = text.replace(`%${index + 1}$`, arg);
        });
        return text;
    };
    return t;
};

// ====================================================================
// 2. بيانات الحجز المحاكاة
// ====================================================================
const MOCK_FLIGHT_DETAIL = {
    carrier: 'Emirates',
    flightNumber: 'EK123',
    route: 'RUH -> DXB',
    departure: '2025-12-01',
    fareBasis: 'Flexible Economy',
    isRefundable: true,
    priceDetails: {
        base_price: 600,
        tax_amount: 30, 
        markup_amount: 15,
        final_price: 645,
    },
    ancillaries: {
        seat: 'Not Selected',
        meal: 'Standard',
        baggage: '20kg Checked',
    }
};

const MOCK_USER_PROFILE = {
    fullName: 'خالد محمد العلي',
    email: 'khaled.m.ali@example.com',
    mobile: '0096650xxxxxx',
    nationality: 'SA',
};

const MOCK_AGENT_INFO = {
    isAgent: true,
    currentBalance: 800,
    creditLimit: 1000,
};

const MOCK_HOTEL = {
    name: "The Smart Resort & Spa",
    location: "Dubai Marina",
    starRating: 5,
    roomType: 'Deluxe Suite',
    checkIn: '2026-03-01',
    checkOut: '2026-03-05',
    nights: 4,
    cancellationPolicy: 'الإلغاء مجاني قبل 72 ساعة.',
    facilities: ['Pool', 'Spa', 'Free WiFi', 'Gym'],
    about: 'فندق فاخر يقع على الواجهة البحرية...',
    nearby: ['Dubai Mall', 'Burj Khalifa'],
    image: 'https://placehold.co/600x400/0d9488/FFFFFF?text=Hotel+Image'
};

// ====================================================================
// 3. المكون الرئيسي
// ====================================================================
const App = () => {
    const [language, setLanguage] = useState('AR'); // حالة اللغة (متطلب اختيار اللغة)
    const t = useTranslation(language); // دالة الترجمة

    const [bookingDetails, setBookingDetails] = useState(MOCK_FLIGHT_DETAIL);
    const [userProfile, setUserProfile] = useState(MOCK_USER_PROFILE);
    const [promoCode, setPromoCode] = useState('');
    const [policyReason, setPolicyReason] = useState('');
    const [isPolicyBreach, setIsPolicyBreach] = useState(false);
    const [selectedPayment, setSelectedPayment] = useState('Credit Card');
    const [message, setMessage] = useState('');
    const [isAgent, setIsAgent] = useState(MOCK_AGENT_INFO.isAgent);

    const isArabic = language === 'AR';

    // محاكاة الإعداد عند التحميل
    useEffect(() => {
        // تحديد اتجاه الصفحة (RTL/LTR)
        document.documentElement.dir = isArabic ? 'rtl' : 'ltr';
        document.documentElement.lang = language.toLowerCase();
        
        // محاكاة التحقق من تجاوز سياسة السعر
        if (bookingDetails.priceDetails.base_price > 550 && !isAgent) {
            setIsPolicyBreach(true);
        }
        
        // محاكاة تنبيه الرصيد للوكيل
        if (isAgent && MOCK_AGENT_INFO.currentBalance < MOCK_AGENT_INFO.creditLimit * 0.5) {
             setMessage(t('logoutAlert', MOCK_AGENT_INFO.currentBalance));
        }
    }, [bookingDetails.priceDetails.base_price, isAgent, isArabic, language]);

    // دالة تحديث الحقول القابلة للتعديل
    const handleProfileChange = (e) => {
        const { name, value } = e.target;
        setUserProfile(prev => ({ ...prev, [name]: value }));
    };

    // دالة محاكاة لتطبيق الكود الترويجي
    const applyPromo = () => {
        if (promoCode === 'SAVE10') {
            const discount = bookingDetails.priceDetails.final_price * 0.10;
            const newPrice = bookingDetails.priceDetails.final_price - discount;
            setBookingDetails(prev => ({
                ...prev,
                priceDetails: {
                    ...prev.priceDetails,
                    final_price: newPrice,
                },
            }));
            setMessage(`✅ ${isArabic ? 'تم تطبيق الخصم بنسبة 10%. السعر الجديد هو' : '10% discount applied. New price is'} ${newPrice.toFixed(2)}$`);
        } else {
            setMessage(t('errorInvalidPromo'));
        }
    };

    // دالة محاكاة لإتمام الحجز
    const handleConfirmBooking = () => {
        if (isPolicyBreach && !policyReason.trim()) {
            setMessage(t('errorPolicyReason'));
            return;
        }
        
        // التحقق من الرصيد للوكلاء
        if (isAgent && bookingDetails.priceDetails.final_price > MOCK_AGENT_INFO.currentBalance) {
             setMessage(t('errorInsufficientBalance', MOCK_AGENT_INFO.currentBalance));
             return;
        }

        setMessage(t('successBooking', selectedPayment));
    };

    const getFinalPrice = () => bookingDetails.priceDetails.final_price.toFixed(2);
    
    // ====================================================================
    // واجهة المستخدم الرسومية (UI)
    // ====================================================================
    return (
        <div className="min-h-screen bg-gray-50 p-4 sm:p-8 font-sans">
            <div className="w-full max-w-6xl mx-auto">
                
                {/* شريط اختيار اللغة (متعدد اللغات) */}
                <div className={`flex justify-end mb-4 ${isArabic ? 'rtl' : 'ltr'}`}>
                    <button 
                        onClick={() => setLanguage('AR')}
                        className={`text-sm py-1 px-3 rounded-l-lg transition duration-150 ${isArabic ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
                    >
                        العربية (AR)
                    </button>
                    <button 
                        onClick={() => setLanguage('EN')}
                        className={`text-sm py-1 px-3 rounded-r-lg transition duration-150 ${!isArabic ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
                    >
                        English (EN)
                    </button>
                </div>

                <h1 className="text-3xl font-extrabold text-indigo-700 mb-2">{t('title')}</h1>
                <p className="text-sm text-gray-500 mb-6 border-b pb-4">{t('subtitle')}</p>

                <div className={`p-3 mb-6 rounded-lg text-sm ${message.startsWith('⚠️') || message.startsWith('خطأ') || message.startsWith('Error') ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'}`}>
                    {message}
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    
                    {/* العمود الأيسر: تفاصيل الحجز */}
                    <div className="lg:col-span-2 space-y-8">

                        {/* 1. تفاصيل الطيران والحجوزات */}
                        <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
                            <h2 className="text-xl font-bold text-gray-800 mb-4">{t('sectionFlight')}</h2>
                            <div className="grid grid-cols-2 gap-y-2 text-sm text-gray-600">
                                <div><span className="font-semibold">{t('carrier')}:</span> {bookingDetails.carrier} ({bookingDetails.flightNumber})</div>
                                <div><span className="font-semibold">{t('route')}:</span> {bookingDetails.route}</div>
                                <div><span className="font-semibold">{t('departureDate')}:</span> {bookingDetails.departure}</div>
                                <div><span className="font-semibold">{t('fareBasis')}:</span> {bookingDetails.fareBasis}</div>
                            </div>
                            
                            <hr className="my-4"/>

                            {/* خيار المقعد والوجبة */}
                            <div className="flex justify-between items-center bg-blue-50 p-3 rounded-lg">
                                <p className="font-medium text-blue-700">{t('ancillaries')}:</p>
                                <button 
                                    onClick={() => setMessage(isArabic ? 'سيتم فتح نافذة اختيار المقاعد والوجبات والأمتعة الإضافية.' : 'A popup for seat, meal, and baggage selection will open.')}
                                    className="text-sm bg-blue-600 text-white py-1 px-4 rounded-lg hover:bg-blue-700 transition"
                                >
                                    {t('selectAncillaries')}
                                </button>
                            </div>
                        </div>
                        
                        {/* 2. تفاصيل الفندق */}
                        <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
                            <h2 className="text-xl font-bold text-gray-800 mb-4">{t('sectionHotel')}: {MOCK_HOTEL.name}</h2>
                            <div className="flex space-x-4 rtl:space-x-reverse">
                                <img src={MOCK_HOTEL.image} alt="Hotel Image" className="w-24 h-24 object-cover rounded-lg"/>
                                <div className="text-sm text-gray-600">
                                    <p><span className="font-semibold">{t('location')}:</span> {MOCK_HOTEL.location}</p>
                                    <p><span className="font-semibold">{t('rating')}:</span> {MOCK_HOTEL.starRating} {isArabic ? 'نجوم' : 'Stars'}</p>
                                    <p><span className="font-semibold">{t('roomType')}:</span> {MOCK_HOTEL.roomType} (4 {isArabic ? 'ليالي' : 'Nights'})</p>
                                    <p className='mt-2'><span className="font-semibold">{t('cancellation')}:</span> {isArabic ? MOCK_HOTEL.cancellationPolicy : 'Free cancellation before 72 hours.'}</p>
                                    <button onClick={() => setMessage(isArabic ? 'عرض خريطة الفندق ومناطق الجذب القريبة' : 'Showing hotel map and nearby attractions.')} className="text-indigo-600 text-xs mt-1 hover:underline">{t('viewMap')}</button>
                                </div>
                            </div>
                        </div>

                        {/* 3. تفاصيل المسافر */}
                        <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
                            <h2 className="text-xl font-bold text-gray-800 mb-4">{t('sectionTraveler')}</h2>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">{t('fullName')}</label>
                                    <input type="text" value={userProfile.fullName} readOnly className="mt-1 w-full px-3 py-2 border rounded-lg bg-gray-100" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">{t('nationality')}</label>
                                    <input type="text" value={userProfile.nationality} readOnly className="mt-1 w-full px-3 py-2 border rounded-lg bg-gray-100" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">{t('email')}</label>
                                    <input 
                                        type="email" 
                                        name="email"
                                        value={userProfile.email} 
                                        onChange={handleProfileChange}
                                        className="mt-1 w-full px-3 py-2 border rounded-lg" 
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">{t('mobile')}</label>
                                    <input 
                                        type="text" 
                                        name="mobile"
                                        value={userProfile.mobile} 
                                        onChange={handleProfileChange}
                                        className="mt-1 w-full px-3 py-2 border rounded-lg" 
                                    />
                                </div>
                            </div>
                        </div>

                        {/* 4. تجاوز سياسة الشركة */}
                        {isPolicyBreach && (
                            <div className="p-4 bg-red-100 border border-red-400 rounded-lg shadow-md">
                                <h3 className="font-bold text-red-700 mb-2">{t('policyBreachTitle')}</h3>
                                <p className="text-sm text-red-600 mb-3">{t('policyBreachText')}</p>
                                <textarea
                                    value={policyReason}
                                    onChange={(e) => setPolicyReason(e.target.value)}
                                    placeholder={t('policyReasonPlaceholder')}
                                    className="w-full px-3 py-2 border border-red-300 rounded-lg"
                                    rows="2"
                                />
                            </div>
                        )}
                    </div>
                    
                    {/* العمود الأيمن: الملخص والدفع */}
                    <div className="lg:col-span-1 space-y-6">
                        
                        {/* ملخص السعر والضرائب */}
                        <div className="bg-gray-100 p-6 rounded-xl shadow-inner">
                            <h2 className="text-xl font-bold text-gray-800 mb-4">{t('summaryTitle', MOCK_AGENT_INFO.currency)}</h2>
                            <div className="space-y-2 text-sm">
                                <div className="flex justify-between"><span>{t('basePrice')}:</span> <span>{bookingDetails.priceDetails.base_price.toFixed(2)}$</span></div>
                                <div className="flex justify-between"><span>{t('taxes')}:</span> <span>{bookingDetails.priceDetails.tax_amount.toFixed(2)}$</span></div>
                                <div className="flex justify-between border-b pb-2"><span>{t('markup')}:</span> <span>{bookingDetails.priceDetails.markup_amount.toFixed(2)}$</span></div>
                                <div className="flex justify-between pt-2 text-lg font-extrabold text-teal-600">
                                    <span>{t('finalTotal')}:</span> <span>{getFinalPrice()}$</span>
                                </div>
                            </div>
                        </div>

                        {/* خيار العروض الترويجية */}
                        <div className="bg-white p-4 rounded-xl shadow-md border border-gray-200">
                            <h3 className="font-semibold text-gray-700 mb-3">{t('promoTitle')}</h3>
                            <div className="flex">
                                <input
                                    type="text"
                                    value={promoCode}
                                    onChange={(e) => setPromoCode(e.target.value)}
                                    placeholder={t('promoPlaceholder')}
                                    className="flex-1 px-3 py-2 border rounded-l-lg focus:ring-indigo-500"
                                />
                                <button
                                    onClick={applyPromo}
                                    className="bg-indigo-600 text-white px-4 py-2 rounded-r-lg hover:bg-indigo-700 transition"
                                >
                                    {t('apply')}
                                </button>
                            </div>
                        </div>

                        {/* خيارات الدفع */}
                        <div className="bg-white p-4 rounded-xl shadow-md border border-gray-200">
                            <h3 className="font-semibold text-gray-700 mb-3">{t('paymentMethod')}</h3>
                            <div className="space-y-2">
                                {[
                                    { id: 'Deposit', label: t('deposit'), balance: MOCK_AGENT_INFO.currentBalance },
                                    { id: 'Credit Card', label: t('creditCard') },
                                    { id: 'Debit Card', label: t('debitCard') },
                                    { id: 'Net Banking', label: t('netBanking') },
                                ].map(method => (
                                    <div key={method.id} className="flex items-center">
                                        <input
                                            type="radio"
                                            id={method.id}
                                            name="payment"
                                            value={method.id}
                                            checked={selectedPayment === method.id}
                                            onChange={(e) => setSelectedPayment(e.target.value)}
                                            className="h-4 w-4 text-indigo-600 border-gray-300 focus:ring-indigo-500 ml-2 rtl:mr-2"
                                        />
                                        <label htmlFor={method.id} className="text-sm font-medium text-gray-700">
                                            {method.label}
                                            {method.id === 'Deposit' && ` (${method.balance}$)`}
                                        </label>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* زر تأكيد الحجز */}
                        <button
                            onClick={handleConfirmBooking}
                            className="w-full py-4 bg-indigo-700 text-white text-xl font-bold rounded-xl shadow-2xl hover:bg-indigo-800 transition duration-200"
                        >
                            {t('confirmPayment')} ({getFinalPrice()}$)
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default App;
