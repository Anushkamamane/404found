import streamlit as st

def analyze_negative_comments(df):
    """
    Analyze negative comments and provide detailed, sales-driven strategies
    for Tata Motors Safari and Harrier. Displays results as styled Streamlit cards
    with clear benefits for each strategy.
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
            strategies["💰 Pricing & Flexible Finance"] = (
                "Offer region-specific EMI plans and loyalty discounts. Introduce subscription models and corporate tie-ups. "
                "Bundle insurance, maintenance, and accessories.\n\n"
                "**Benefit:** Increased affordability → More buyers can afford your vehicles, boosting sales volume and market penetration."
            )

        # ---------------- SERVICE & AFTER-SALES ----------------
        elif "service" in c or "maintenance" in c or "repair" in c:
            strategies["🛠️ Service & After-Sales Excellence"] = (
                "Provide doorstep service and predictive maintenance using IoT. Launch premium service subscriptions and loyalty points.\n\n"
                "**Benefit:** Higher customer satisfaction → Improved retention and repeat purchases, leading to stronger long-term sales."
            )

        # ---------------- FEATURES & TECH ----------------
        elif "feature" in c or "missing" in c or "technology" in c:
            strategies["⚡ Tech & Features Enhancement"] = (
                "Launch special editions with latest tech features, over-the-air updates, and 3D configurators.\n\n"
                "**Benefit:** Tech-savvy buyers attracted → Drives showroom visits, increases conversion rates, and positions brand as innovative."
            )

        # ---------------- DELIVERY & AVAILABILITY ----------------
        elif "delivery" in c or "wait" in c or "delay" in c:
            strategies["🚚 Delivery & Availability"] = (
                "Improve stock using AI demand forecasting, micro-hubs, and real-time delivery tracking. Offer early-bird incentives.\n\n"
                "**Benefit:** Faster delivery and reduced waiting → Enhances customer satisfaction and converts leads faster, boosting sales."
            )

        # ---------------- COMPETITOR COMPARISON ----------------
        elif "competitor" in c or "better than" in c:
            strategies["📈 Competitive Advantage & Branding"] = (
                "Highlight Safari & Harrier strengths: safety, performance, premium design. Run comparative campaigns with testimonials.\n\n"
                "**Benefit:** Buyers see clear advantages → Increases market share and sways potential buyers from competitors."
            )

        # ---------------- FUEL & EFFICIENCY ----------------
        elif "fuel" in c or "efficiency" in c or "mileage" in c:
            strategies["⛽ Fuel Efficiency & Eco Options"] = (
                "Promote hybrid/mild-electric variants and trade-in discounts. Showcase mileage with AI-driven reports.\n\n"
                "**Benefit:** Eco-conscious and cost-aware buyers convinced → Expands target audience and increases vehicle adoption."
            )

        # ---------------- COMFORT & SPACE ----------------
        elif "comfort" in c or "space" in c or "seating" in c:
            strategies["🛋️ Comfort & Luxury"] = (
                "Enhance interiors with premium materials and VR cabin configurators. Bundle comfort-focused trims.\n\n"
                "**Benefit:** Buyers experience tangible luxury → Encourages upgrades to higher trims and increases average revenue per vehicle."
            )

        # ---------------- DESIGN & STYLE ----------------
        elif "design" in c or "looks" in c or "style" in c:
            strategies["🎨 Design & Aesthetic Innovation"] = (
                "Launch limited edition colors/trims and co-creation contests.\n\n"
                "**Benefit:** Creates exclusivity and emotional attachment → Drives showroom traffic and encourages quicker buying decisions."
            )

        # ---------------- SAFETY ----------------
        elif "safety" in c or "accident" in c or "crash" in c:
            strategies["🛡️ Safety & Reliability"] = (
                "Promote advanced safety features and extended warranties.\n\n"
                "**Benefit:** Builds trust with buyers → Attracts family buyers and safety-conscious segments, increasing conversion."
            )

        # ---------------- ENGINE & PERFORMANCE ----------------
        elif "engine" in c or "performance" in c:
            strategies["⚙️ Performance & Driving Experience"] = (
                "Highlight turbocharged engines, ride dynamics, and handling. Offer performance packages.\n\n"
                "**Benefit:** Enthusiasts and SUV lovers engaged → Increases test drives and higher trim sales."
            )

        # ---------------- RESELL VALUE ----------------
        elif "resale" in c or "value" in c or "depreciation" in c:
            strategies["🔄 Resale & Value Retention"] = (
                "Guaranteed buyback programs and blockchain-based vehicle history tracking.\n\n"
                "**Benefit:** Reduces purchase hesitation → Encourages buyers who value long-term investment, increasing sales."
            )

        # ---------------- DIGITAL MARKETING ----------------
        elif "ads" in c or "promotion" in c or "campaign" in c:
            strategies["📱 Digital & Social Marketing"] = (
                "AI-optimized ads, AR/VR campaigns, gamified referral programs.\n\n"
                "**Benefit:** Engages digital audience → Expands reach, drives showroom visits, and converts leads faster."
            )

        # ---------------- SALES-FOCUSED ADDITIONAL STRATEGIES ----------------
        else:
            strategies["🚀 Sales Growth & Conversion"] = (
                "Personalized AI recommendations, limited-time bundles, influencer campaigns, test-drive festivals, loyalty programs.\n\n"
                "**Benefit:** Directly boosts conversions → Converts leads faster, increases high-trim sales, and grows repeat buyers."
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
