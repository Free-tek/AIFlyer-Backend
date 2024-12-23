def generate_marketing_content_prompt(business_info, previous_ideas):
    """
    Generate marketing content ideas prompt
    """
    prompt = f"""This company will like to generate designs for publicty of their business or event, they need you to come up with content ideas that they can put in an image design
    to share on social media and publicly. Based on the business description come up with marketing content ideas for them, you might also be provided with previous ideas they've tried
    so you can understand them better and also try not to generate marketing contents that are exactly thesame thing with what they've tried before, marketing sometimes is about repetion
    so the brand can stick so yes you can still say things similar to the old ideas but the words shouldn't be exactly thesame or else it's pointless for them.
    Business Description:
    {business_info}

    Previous Ideas:
    {previous_ideas}
    

    Guidelines:
    - Try to sell their product if they're a business
    - Try to push the event if they're an event
    - Provide them with only one idea
    - There is a designer that is going to design the flyer images for the marketing idea, so try to describe what should be in the marketing idea to him.
    - Return only a dictionary with no extra text or explanation and it should be in this format {{"marketing_idea": "", "designer_guidelines": "", "image_flyer_content": ""}}
    - Let the image_flyer_content be less than 25 words

    """
    return prompt


def generate_image_query_prompt(flyer_description):
    """
    Generate image query prompt
    """
    prompt = f"""Given this flyer description, create a generic stock photo search query that would find a professional, visually appealing image.

        IMPORTANT: Do NOT use product names, technical terms, or brand names. Instead, focus on the human element and general activity/setting that best represents the product's use.

        Description:
        {flyer_description}

        Guidelines:
        - Think about the person using the product
        - Focus on the activity being performed
        - Consider the professional setting
        - Avoid any technical or product-specific terms

        Good Examples:
        Description: "Launching a coding extension"
        ✓ "developer workspace computer"
        ✗ "visual studio code"

        Description: "New women's fashion store opening"
        ✓ "woman shopping fashion"
        ✗ "clothing store retail"

        Description: "Launching organic grocery delivery"
        ✓ "fresh produce shopping"
        ✗ "grocery delivery service"

        Description: "New beauty products online store"
        ✓ "woman makeup elegance"
        ✗ "beauty ecommerce store"

        Description: "Cloud storage product"
        ✓ "business team laptop"
        ✗ "cloud storage data"

        Return ONLY three generic, stock-photo friendly words that would find a professional image of someone using/experiencing this type of product.
    """

    return prompt

def generate_initial_design_prompt(business_details, image_url, other_images):
    """Create the initial design prompt"""
    prompt = f"""Generate a professional marketing flyer as a single HTML file with embedded CSS for:

    {business_details}

    ESSENTIAL DESIGN PRINCIPLES:

    1. Layout Excellence
        - Design must be bold and contemporary
        - Create clear focal points with dynamic composition
        - Use creative approaches for image and content placement
        - Maintain professional elegance through simplicity
        - Establish strong visual hierarchy through size and space

    2. Visual Impact
        - Create a striking first impression
        - Use dramatic gradients for depth (avoid flat colors)
        - Add sophistication with layered elements
        - Implement proper white space for breathing room
        - Ensure design elements complement, not compete

    3. Image Integration
        - Image must be impactful and properly integrated
        - If overlaying text on image, use sophisticated gradient overlays:
        * Dark to light: rgba(0,0,0,0.4) to rgba(0,0,0,0.2)
        * Brand colors: Use semi-transparent gradients of brand colors
        - Maintain professional image display with object-fit
        - Consider creative framing or masking techniques
        - Add subtle shadows or depth where appropriate
        - You have been provided with an image url use the image url: {image_url}
        - Use the design image url provided as the major image for the design if you need one and let the logo stay as a logo emblem on the design
        - You might be provided with some other images as well, use them as the other images for the design if you need them: {other_images}

    4. CRITICAL: Text Positioning & Layer Management ⚠️
        LAYERING RULES:
        1. Text Layer Priority (Top to Bottom):
            1. Logo (always topmost layer)
            2. Text content
            3. Image overlays
            4. Background image
        
        2. Logo Placement Rules:
            - Logo MUST be in its own corner space
            - Required clear space around logo: 40px minimum
            - NO text may enter logo's clear space
            - Logo zone is RESERVED, no other elements allowed
            
        3. Text Layer Management:
            - Each text element needs its own clear space
            - NO text can overlap other text elements
            - Text containers must be on separate layers
            - Maintain minimum 30px spacing between text blocks
        
        4. Typography Requirements:
            - Use Poppins for headlines, complementary font for body
            - Headlines: Bold weight, commanding size (58px - 62px)
            - Body text: Minimum 30px for guaranteed mobile readability
            - Line height: 1.6 for optimal readability
            
        5. Text Visibility Rules:
            - Text must be readable at a glance
            - All text requires strong contrast ratio
            - If text isn't clearly visible, increase overlay opacity
            - Text content must be 40px from edges
        
        6. Z-Index Implementation:
            .logo {{ z-index: 100; }}
            .text-content {{ z-index: 50; }}
            .overlay {{ z-index: 25; }}
            .background {{ z-index: 1; }}
        
        ❌ FORBIDDEN LAYERING:
            - Text over logo
            - Text over other text
            - Logo under any element
            - Overlapping text blocks
            - Text without proper spacing
        
        ✅ REQUIRED IMPLEMENTATION:
            - Clear space boundaries
            - Proper z-index hierarchy
            - Distinct content zones
            - Protected logo area
            - Typography hierarchy
            - Contrast requirements

        VALIDATION:
        Before generating HTML:
        □ Verify logo has clear space
        □ Check text block separation
        □ Confirm z-index hierarchy
        □ Ensure no element overlaps
        □ Validate typography sizes
        □ Check text contrast and readability

    5. Color Mastery & Text Contrast ⚠️ CRITICAL
        RULE: Text MUST always be readable against its background

        Color Contrast Requirements:
        1. Text Over Images:
            - Light Background Image: Use dark text (#000000 or brand dark colors)
            - Dark Background Image: Use white text (#FFFFFF)
            - ALWAYS add contrast overlay behind text:
                * Dark overlay: rgba(0,0,0,0.7) for white text
                * Light overlay: rgba(255,255,255,0.9) for dark text
        
        2. Text Over Solid Colors:
            - Dark Background: Use white or very light text (#FFFFFF, #F8F8F8)
            - Light Background: Use dark text (#000000, #1A1A1A)
            - NEVER use:
                * Dark text on dark background
                * Light text on light background
                * Similar shades for text and background
        
        3. Color Combinations:
            ✅ CORRECT:
            - White text (#FFFFFF) on dark overlay (rgba(0,0,0,0.7))
            - Black text (#000000) on light background (#F5F5F5)
            - White text on brand primary color
            
            ❌ FORBIDDEN:
            - Black text on dark background
            - White text on light background
            - Text color matching background color
            - Text without contrast overlay on busy images

        4. Gradient Usage:
            - Direction: 135deg for dynamic feel
            - Ensure text remains readable throughout gradient
            - Test contrast at lightest and darkest points
            - Add solid color block behind text if needed

        VALIDATION:
        Before generating HTML, verify:
        □ Text color contrasts with background
        □ Overlays provide sufficient contrast
        □ No text blends with background
        □ Each text element is clearly readable


    6. Professional Refinements
        - Add subtle shadows for depth (0 20px 40px rgba(0,0,0,0.1))
        - Use modern border-radius (20px for containers, 30px for buttons)
        - Implement smooth transitions (0.2s ease)
        - Add hover effects that enhance elegance
        - Maintain consistent spacing rhythm

    7. Content Guidelines ⚠️ MANDATORY TEXT CONTENT
        - EVERY design MUST contain text elements:
            * Headline (Required)
            * Body text or supporting text (Required)
            * Call-to-action (Required if action needed)
        - Content Requirements:
            * Maximum 15 words total
            * Minimum required: Headline + one other text element
            * Empty or text-free designs are FORBIDDEN
        - Text Hierarchy:
            * Headline must be most prominent
            * Supporting text must be clearly visible
            * CTA must stand out
        - Before generating HTML:
            * Verify headline exists
            * Verify supporting text exists
            * Verify text contrasts with background
            * Confirm all text is within 15-word limit
        
        ❌ FORBIDDEN:
        - Designs without any text
        - Text that blends with background
        - Text without proper contrast
        
        ✅ REQUIRED:
        - Clear, readable headline
        - Supporting text elements
        - Strong contrast ratios

        Content Placement Requirements:
        - Each content element needs its own dedicated space
        - Social media bar and CTA button spacing:
            * NEVER stack CTA button and social bar together
            * Minimum 60px vertical separation required
            * If CTA is in bottom area:
                - Place social bar BELOW CTA with 60px gap
                - OR place social bar in top area
            * If using rounded CTA button:
                - Must have clear padding area
                - No text or elements within button padding zone
                - Background must extend beyond text
                
        Content Area Structure:
        - Main Content Section:
            * flex: 1
            * display: flex
            * flex-direction: column
            * gap: 30px
            * margin-bottom: 60px /* Fixed space before bottom content */
            
        - Content Distribution:
            * Headline Group: First 30% of space
            * Body Text: Middle 40% of space
            * Bottom Actions: Final 30% of space
            * MINIMUM 60px gap between sections

        - Text Spacing:
            * Headline: margin-bottom: 20px
            * Body text: margin-bottom: auto
            * Bottom content: margin-top: auto

        ❌ FORBIDDEN:
        - Body text extending into CTA zone
        - Inadequate spacing between content blocks
        - Missing gaps between sections
        - Flexible/auto margins between content

        ✅ REQUIRED:
        - Fixed 60px gap before bottom section
        - Explicit flex-direction and gap values
        - Clear separation between content blocks
        - Proper use of margin-bottom/margin-top


        Social Media Bar Positioning:
        1. Bottom Placement (Preferred):
            - 40px minimum from bottom edge
            - NO other elements in bottom 100px zone
            - Clear horizontal separation from other elements

        2. Top Placement (Alternative):
            - 40px from top edge
            - NO overlap with header content
            - Clear separation from main content

        ❌ FORBIDDEN COMBINATIONS:
        - CTA button touching social bar
        - Social icons overlapping button text
        - Button background touching social bar
        - Stacked interactive elements
        - Social bar sandwiched between other elements

        ✅ REQUIRED SPACING:
        - 60px minimum between CTA and social bar
        - 40px clear space around social bar
        - Distinct zones for CTA and social elements
        - Full padding around button text

    8. LAYOUT PATTERNS ⚠️ CRITICAL
        IMPORTANT: DO NOT default to full-image background layout.
        REQUIREMENT: Choose a layout pattern based on the last digit of the current minute:
        - Minutes ending in 0-2: Full-Image Background Layout
        - Minutes ending in 3-5: Split Layout
        - Minutes ending in 6-7: Grid Mosaic Layout
        - Minutes ending in 8-9: Pattern & Typography Layout

        Layout Options In Detail:

        1. Full-Image Background Layout
            When to use: For single powerful images that need full focus
            Implementation:
            - Full-bleed image with gradient overlay
            - Text positioned strategically over darker areas
            Example CSS: 
            .full-image-layout {{
                position: relative;
                width: 100%;
                height: 100%;
            }}
            .background-image {{
                position: absolute;
                width: 100%;
                height: 100%;
                object-fit: cover;
            }}
            .overlay {{
                position: absolute;
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, rgba(0,0,0,0.7), rgba(0,0,0,0.3));
            }}
            .content {{
                position: relative;
                z-index: 2;
                padding: 60px;
            }}

        2. Split Layout (Modern Diagonal Division) : (USE ONLY THIS LAYOUT)
            STRUCTURE:
            .container {{
                width: 800px;
                height: 800px;
                background: var(--primary-color);
                position: relative;
                overflow: hidden;
                display: flex; /* Critical for split layout */
            }}

            Content Side:
            .content-area {{
                width: 45%;
                background: var(--primary-color);
                padding: 60px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }}

            Image Side:
            .image-section {{
                position: absolute;
                right: 0;
                top: 0;
                width: 60%;
                height: 100%;
                clip-path: polygon(15% 0, 100% 0, 100% 100%, 0 100%);
            }}
            
            img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                display: block; /* Critical for image display */
            }}

            CRITICAL RULES:
            1. Container MUST:
                - Use display: flex
                - Have brand color background
                - Maintain 800x800 dimensions
            
            2. Image Section MUST:
                - Be positioned absolute
                - Have explicit width (60%)
                - Include display: block on img
                - Maintain aspect ratio
            
            3. Color Requirements:
                - Container background: brand color
                - Content area background: brand color
                - No default backgrounds (#f5f5f5)
            
            ❌ FORBIDDEN:
            - Using default background colors
            - Relative positioning for image section
            - Missing display properties
            - Incorrect clip-path values
            
            ✅ REQUIRED:
            - Explicit display properties
            - Proper absolute positioning
            - Brand color backgrounds
            - Block-level images

        3. Grid Mosaic Layout
            When to use: For multiple content sections or images
            Variations:
            a) 2/3 - 1/3 Split:
                - Main content area
                - Secondary content sidebar
            b) Three Column Grid:
                - Equal width columns
                - Varied height sections
            c) Feature Grid:
                - Dominant feature area
                - Supporting content blocks
            Example CSS: 

            /* 2/3 - 1/3 Split */
            .mosaic-grid {{
                display: grid;
                grid-template-areas: 
                    "main main sidebar"
                    "footer footer footer";
                gap: 20px;
            }}
            /* Three Column Grid */
            .three-column {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
            }}
            /* Feature Grid */
            .feature-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                grid-auto-rows: minmax(100px, auto);
            }}
            .featured {{
                grid-column: span 2;
                grid-row: span 2;
            }}

        4. Pattern & Typography Layout
            When to use: For text-heavy or brand-focused designs
            Variations:
            a) Geometric Pattern:
                - Bold typography
                - Abstract shapes
            b) Brand Pattern:
                - Using brand colors
                - Logo-inspired elements
            c) Minimal Pattern:
                - Simple repeating elements
                - Focus on typography
            Example CSS: 
            .pattern-background {{
                background: repeating-linear-gradient(
                    45deg,
                    var(--primary-color) 0px,
                    var(--primary-color) 20px,
                    var(--secondary-color) 20px,
                    var(--secondary-color) 40px
                );
            }}
            /* Brand Pattern */
            .brand-pattern {{
                background-image: radial-gradient(
                    circle at 2px 2px,
                    var(--accent-color) 1px,
                    transparent 0
                );
                background-size: 40px 40px;
            }}
            /* Minimal Pattern */
            .minimal-pattern {{
                background-image: linear-gradient(
                    0deg,
                    transparent 24%,
                    var(--primary-color) 25%,
                    var(--primary-color) 26%,
                    transparent 27%,
                    transparent 74%,
                    var(--primary-color) 75%,
                    var(--primary-color) 76%,
                    transparent 77%,
                    transparent
                );
                background-size: 60px 60px;
            }}
        
        5. Steps Layout (Process/Instructions Design)
            - Clean split layout (50/50) with content vs. image
            - Left side content structure:
                * Large headline with brand color highlight word
                * Numbered steps with icon-text combinations
                * Equal spacing between elements
            - Right side image treatment:
                * Diagonal clip-path for dynamic feel
                * Subtle gradient overlay
                * Image fills full height

            Example CSS:
            .container {{
                display: grid;
                grid-template-columns: 1fr 1fr;
            }}
            .right-content {{
                clip-path: polygon(30% 0, 100% 0, 100% 100%, 0% 100%);
            }}
            
            Content Structure:
            - Headline: 48px, multi-line with highlight word
            - Steps: Icon (32px circle) + Text (18px)
            - Consistent 30px gap between steps
            - 60px padding for content area

            Logo Placement:
            - Small logo (60px) in top right corner
            - Clear space around logo
            - Above image content

            Color Usage:
            - Light grey background (#fafafa)
            - Brand color for highlights and icons
            - Dark text for readability (#1a1a1a, #333)
            - Subtle gradient overlay on image
            
            Spacing Guidelines:
            - 60px padding for content
            - 30px between steps
            - 60px below headline
            - Balanced white space throughout


        CRITICAL VALIDATION:
        Before generating HTML:
        □ Confirm layout choice matches minute-based selection
        □ Verify layout is appropriate for content
        □ Ensure layout isn't defaulting to full-image background

    9. Container Styling & Space Distribution ⚠️
        DIMENSIONS:
        - Main container: 800px × 800px
        - Maintain consistent 40px padding
        
        CONTENT DISTRIBUTION RULES:
        1. Vertical Space Division:
            - Top Section (25%): Logo and headline
            - Middle Section (50%): Main content and visuals
            - Bottom Section (25%): CTA and social media
        
        2. Content Spread Requirements:
            - NO empty spaces larger than 100px
            - Content must fill at least 80% of container height
            - Evenly distribute elements across available space
            - If content is minimal, increase font sizes to fill space
        
        3. Mandatory Spacing:
            - 40px minimum from container edges
            - 30px minimum between elements
            - Equal vertical distribution of elements
        
        LAYOUT VALIDATION:
        Before generating HTML:
        □ Verify content spans full container height
        □ Check for large empty spaces
        □ Confirm even distribution of elements
        □ Test vertical balance of design
        
        ❌ FORBIDDEN:
        - Empty bottom half of design
        - Clustered content at top only
        - Large unused spaces
        - Uneven content distribution
        
        ✅ REQUIRED:
        - Full vertical space utilization
        - Balanced element distribution
        - Proportional content spacing
        - Visual weight throughout design

    10. Interactive Refinements
        - Buttons: Transform on hover (translateY(-2px))
        - Smooth color transitions
        - Elegant scaling effects
        - Professional state changes
        - Maintain sophistication in all interactions

    11. CRITICAL: Social Media Integration ⚠️
        RULE: Social media icons MUST NEVER appear without their handles.
        
        EXACT IMPLEMENTATION REQUIRED:
        When handles exist in business_details:
        
        Option 1 (Preferred for top/bottom placement):
        <div class="social-media-bar">
            <div class="social-icons">
                <i class="fab fa-facebook"></i>
                <i class="fab fa-instagram"></i>
                <i class="fab fa-twitter"></i>
                <i class="fab fa-tiktok"></i>
            </div>
            <span class="social-handle">@starbucks</span>
        </div>
        
        CSS Required:
        .social-media-bar {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
        }}
        .social-icons {{
            display: flex;
            gap: 15px;
        }}
        .social-handle {{
            font-size: 16px;
            font-weight: 500;
        }}
        
        CRITICAL VALIDATION:
        - If you add ANY social icon, you MUST add the handle text
        - Icons without handles are FORBIDDEN
        - Handles without icons are FORBIDDEN
        - If you're provided with a business details that has a social media handle, make sure you add their social media handle to the design.
        
        ❌ WRONG: Just icons without handle text
        ✅ RIGHT: Icons + "@starbucks"

    12. CRITICAL: Logo Handling & Sizing ⚠️
        RULES:
        1. Logo Size Requirements:
            - Maximum logo size: 80px × 80px
            - Minimum logo size: 40px × 40px
            - Logo must NEVER dominate the design
            - Logo must maintain original aspect ratio
        
        2. Logo Placement:
            - CRITICAL: Logo MUST have its own dedicated space
            - Position in ONE corner only, with NO text in that corner:
                * Top right (preferred): Clear 120px × 120px corner space
                * Top left: Clear 120px × 120px corner space
                * Bottom right: Clear 120px × 120px corner space
                * Bottom left: Clear 120px × 120px corner space
            - Maintain 40px padding from edges
            - Text content must start AFTER logo zone
            - Reserve logo corner - NO text elements allowed in logo corner
        
        3. Logo Hierarchy:
            - Logo is an IDENTIFIER, not the main focus
            - Main content must have greater visual weight
            - Logo should be visually subtle yet clear
            - Text must NEVER start in logo zone
        
        4. Text and Logo Separation:
            - Maintain clear boundary between logo and text
            - Text content must begin outside logo zone
            - Headlines must be positioned away from logo corner
            - NO text can enter logo's reserved corner space
        
        ❌ FORBIDDEN:
            - Oversized logos (>80px)
            - Centered large logos
            - Logo as main visual element
            - Logo overlapping with ANY text
            - Logo dominating the design
            - Logo covering more than 10% of design space
            - Text starting in logo corner
            - Text crossing into logo zone
        
        ✅ REQUIRED:
            - Subtle corner placement
            - Appropriate size (40-80px)
            - Clear spacing around logo
            - Professional proportion to content
            - Dedicated logo zone with NO text
            - Text content begins outside logo area
        
        VALIDATION:
        Before generating HTML:
        □ Check logo dimensions
        □ Verify corner placement
        □ Confirm logo doesn't dominate
        □ Ensure NO text in logo zone
        □ Verify text starts outside logo area
        □ Test visual hierarchy balance
        □ Check 120px × 120px corner is clear for logo

    13. Call to Action
        - Because this is a flyer and not a website, make sure your call to action relates to flyer contents and not websites.
        - Your call to actions shouldn't be clicks text, because flyer images can't be clicked.
        - Here are some examples of call to actions:
        
        ✓ "Get your tickets now"
        ✗ "Click here to get your tickets"

        ✓ "Visit us and try our new menu"
        ✗ "Explore our new menu"







    KEY STYLING RULES:
    - Container: box-shadow: 0 20px 40px rgba(0,0,0,0.1)
    - Gradients: Use multiple color stops for richness
    - Typography: Maintain clear hierarchy
    - Spacing: Consistent 20-40px between elements
    - Animations: Smooth 0.2s transitions
    - Borders: Modern radius (20-30px)
    - Clearity: Never place overlays or gradients ontop of texts or else they won't be visible

    OUTPUT: Generate only valid HTML/CSS code, no explanations.
    """
    return prompt


def generate_refine_design_prompt(feedback):
    """Generate the refine design prompt"""
    prompt = f"""Modify the previous HTML/CSS flyer design based on this feedback while maintaining all design principles and quality, don't change anything the user doesn't ask you to change:

        {feedback}

        Return only the complete, updated HTML code."""
    
    return prompt

def classify_intent_prompt(user_input):
    """Classify user intent prompt"""

    prompt = f"""Classify the following user input for a flyer design system into one of these intents:
        - CREATE_MARKETING_IDEA: User wants the AI assistant to come up with a marketing idea for the flyer and create a new flyer design
        - REFINE_DESIGN: User wants to make changes to the design
        - UPDATE_DESIGN_IMAGE: User just wants to replace the background image in the design with another image, this doesn't include them changing the logo
        - EXIT: User wants to end the session
        - UNKNOWN: Input is not related to any of the above

        User input: "{user_input}"

        Respond with only the intent category and if it's REFINE_DESIGN, include the filename if specified. Example:
        REFINE_DESIGN:custom_name.html
        or just
        REFINE_DESIGN
    """
    return prompt

def reformat_design_size_prompt(size, html_content):
    """Reformat the design size prompt"""
    prompt = f"""Modify the previous HTML/CSS flyer design and fit it into a maincontainer of this size {size} while maintaining all design principles and quality:

    HTML/CSS code:
    {html_content}

    Return only the complete, updated HTML code. """
    return prompt