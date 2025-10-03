import streamlit as st

def analyze_negative_comments(df):
    """
    Analyze negative comments and provide detailed, sales-driven strategies
    for Tata Motors Safari and Harrier. Displays results as styled Streamlit cards.
    """
    strategies = {}

    # Detect which column contains comments
    if 'translated_message' in df.columns:
        comments = df['translated_message']
    elif 'message' in df.columns:
        comments = df['message']
    elif 'translated_comment' in df.columns:
        comments = df['translated_comment']
    elif 'comment' in df.columns:
        comments = df['comment']
    elif 'text' in df.columns:
        comments = df['text']
    else:
        raise KeyError("No suitable comment column found in DataFrame")

    for comment in comments:
        c = comment.lower() if isinstance(comment, str) else ''
        
        # ---------------- PRICING & FINANCE ----------------
        if "cost" in c or "price" in c or "expensive" in c:
            strategies["💰 Pricing & Finance Strategy"] = (
                "Implement flexible subscription models and personalized EMI plans for Safari & Harrier. "
                "Offer loyalty discounts for repeat buyers and corporate tie-ups. Leverage AI-driven pricing "
                "to ensure competitive positioning across regions. Introduce value-added bundles like insurance, "
                "maintenance, and accessories for higher perceived value. Launch targeted campaigns highlighting "
                "cost-effectiveness compared to competitors."
            )

        # ---------------- SERVICE & AFTER-SALES ----------------
        elif "service" in c or "maintenance" in c or "repair" in c:
            strategies["🛠️ Service & After-Sales Excellence"] = (
                "Introduce premium service packages with guaranteed turnaround times and IoT-based predictive maintenance "
                "alerts. Provide doorstep service and AR-assisted virtual troubleshooting. Implement a digital loyalty "
                "program rewarding customers for regular maintenance. Highlight after-sales success stories in social media campaigns."
            )

        # ---------------- FEATURES & TECH ----------------
        elif "feature" in c or "missing" in c or "technology" in c:
            strategies["⚡ Advanced Features & Technology"] = (
                "Upgrade Safari & Harrier with AI-powered safety and driver assistance, connected infotainment, "
                "and smart navigation. Introduce over-the-air updates to continuously improve user experience. "
                "Bundle new tech features as part of special editions to drive showroom traffic. Promote these "
                "innovations via influencer campaigns and virtual test drives."
            )

        # ---------------- DELIVERY & AVAILABILITY ----------------
        elif "delivery" in c or "wait" in c or "delay" in c:
            strategies["🚚 Delivery & Availability Optimization"] = (
                "Use AI-powered demand forecasting to reduce waiting periods. Increase stock availability at key showrooms "
                "and leverage micro-distribution hubs. Implement real-time tracking and proactive customer notifications. "
                "Offer incentives for early bookings and pre-orders to manage high demand efficiently."
            )

        # ---------------- COMPETITOR COMPARISON ----------------
        elif "competitor" in c or "better than" in c:
            strategies["📈 Competitive Positioning & Branding"] = (
                "Highlight Safari & Harrier strengths: safety, robust build, premium features, and superior ride quality. "
                "Launch comparative campaigns showcasing advantages over competitors. Utilize customer testimonials, "
                "video reviews, and social proof. Implement localized branding for key regions to strengthen market share."
            )

        # ---------------- FUEL & EFFICIENCY ----------------
        elif "fuel" in c or "efficiency" in c or "mileage" in c:
            strategies["⛽ Fuel Efficiency & Eco-Friendly Options"] = (
                "Promote hybrid or mild-electric versions for higher fuel efficiency. Provide loyalty programs for eco-conscious customers. "
                "Showcase Safari & Harrier mileage performance in social media campaigns. Introduce trade-in offers for fuel-inefficient vehicles."
            )

        # ---------------- COMFORT & SPACE ----------------
        elif "comfort" in c or "space" in c or "seating" in c:
            strategies["🛋️ Comfort, Space & Luxury"] = (
                "Enhance interiors with premium upholstery, ambient lighting, and ergonomic seating. "
                "Offer virtual reality cabin configurators online to showcase customization options. "
                "Bundle comfort-focused packages for premium trims to increase sales appeal."
            )

        # ---------------- DESIGN & STYLE ----------------
        elif "design" in c or "looks" in c or "style" in c:
            strategies["🎨 Design & Aesthetic Innovation"] = (
                "Offer limited edition Safari & Harrier variants with unique color palettes and exterior trims. "
                "Run social campaigns highlighting modern design, rugged yet premium aesthetics. "
                "Engage customers with co-creation contests for styling ideas."
            )

        # ---------------- SAFETY ----------------
        elif "safety" in c or "accident" in c or "crash" in c:
            strategies["🛡️ Safety & Reliability"] = (
                "Promote advanced safety features like multiple airbags, ABS, ESC, lane assist, and emergency braking. "
                "Publish independent crash test results and reliability ratings to build trust. "
                "Offer extended safety warranties to reinforce long-term confidence."
            )

        # ---------------- ENGINE & PERFORMANCE ----------------
        elif "engine" in c or "performance" in c:
            strategies["⚙️ Performance & Driving Experience"] = (
                "Highlight turbocharged engines, smooth ride dynamics, and handling capabilities. "
                "Offer test-drive campaigns emphasizing SUV performance. "
                "Introduce special performance packs for enthusiasts and create digital simulations showcasing engine efficiency."
            )

        # ---------------- RESELL VALUE ----------------
        elif "resale" in c or "value" in c or "depreciation" in c:
            strategies["🔄 Resale & Value Retention"] = (
                "Launch guaranteed buyback programs for Safari & Harrier. "
                "Provide blockchain-based vehicle history tracking to increase transparency. "
                "Highlight low depreciation rate and long-term ownership value in campaigns."
            )

        # ---------------- CUSTOMER ENGAGEMENT ----------------
        else:
            strategies["🤝 Customer Engagement & Loyalty"] = (
                "Use AI to analyze feedback and personalize offers. "
                "Run community engagement campaigns, owner clubs, and referral incentives. "
                "Offer concierge-level digital support to create brand evangelists."
            )

    # ---- Render unique strategies as Streamlit cards ----
    for title, text in strategies.items():
        st.markdown(
            f"""
            <div style="
                background-color:#f0f8ff;
                border:1px solid #aad4ff;
                border-radius:12px;
                padding:20px 25px;
                margin-bottom:18px;
                box-shadow:0 3px 6px rgba(0,0,0,0.08);
            ">
                <h4 style="color:#1769aa; margin-bottom:10px;">{title}</h4>
                <p style="color:#222; font-size:15.5px; line-height:1.5;">{text}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    return strategies
