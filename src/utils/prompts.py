def generate_marketing_content_prompt(business_info, previous_ideas):
    """
    Generate marketing content ideas prompt
    """
    prompt = f"""This company will like to generate designs for publicty of their business or event, they need you to come up with content ideas that they can put in an image design
    to share on social media and publicly. Based on the business description come up with marketing content ideas for them, you might also be provided with previous ideas they've tried
    so you can understand them better and also try not to generate marketing contents that are exactly thesame thing with what they've tried before, marketing sometimes is about repetion
    so the brand can stick, so yes you can still say things similar to the old ideas but the words shouldn't be exactly thesame or else it's pointless for them.
    Business Description:
    {business_info}

    Previous Ideas:
    {previous_ideas}

    You'll also be provided with a list of design layouts that can be used to design the flyer, based on how you'll like the design to look you'll pick which of this layout designs you want to use for the marketing idea.
    Layout Options:
    {layout_types}

    Guidelines:
    - Try to sell their product if they're a business
    - Try to push the event if they're an event
    - Provide them with only one idea
    - There is a designer that is going to design the flyer images for the marketing idea, so try to describe what should be in the marketing idea to him.
    - Select a layout type from the layout options provided and pick the layout_name from the layout_types dictionary.
    - Return only a dictionary with no extra text or explanation and it should be in this format {{"marketing_idea": "", "designer_guidelines": "", "image_flyer_content": "", "layout_name": "the name of the layout, must match how it's written in the layout_types dictionary"}}
    - Let the image_flyer_content be less than 25 words

    """
    return prompt



def generate_thumbnail_caption_prompt(video_description):
    prompt = f"""
    Generate viral-worthy TikTok thumbnail text based on the video content description.
    You'll be provided with a video description and you should create engaging, Gen-Z optimized text for the thumbnail.

    Video Description:
    {video_description}

    Guidelines:
    - Create short, punchy text (max 2-3 lines)
    - Use impactful, emotional words (SHOCKED, EMOTIONAL, INSANE, etc.)
    - Include 2-4 relevant emojis strategically placed
    - Focus on reaction/emotion rather than description
    - Use all caps for maximum impact
    - If featuring celebrities/influencers, use their known nicknames/handles
    
    Examples of Good Thumbnails:
    ✅ "MILLIONAIRE CHANGED MY LIFE! 🤯💰"
    ✅ "SHE SAID YES! 💍 *EMOTIONAL*"
    ✅ "MEETING MY IDOL 😱 (GONE WRONG)"
    
    Examples to Avoid:
    ❌ "Meeting a famous footballer today"
    ❌ "New video with special guest"
    ❌ "Watch what happened next"

    Return only a dictionary in this format:
    {{
        "main_text": "FIRST LINE OF TEXT",
        "highlight_text": "OPTIONAL SECOND LINE", 
        "emojis": ["emoji1", "emoji2"],
        "corner_emoji": "special_emoji #iconic corner placements like 🐐 but optional",   
        "text_position": "center | bottom-center | top-center"
    }}
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


def generate_thumbnail_image_query_prompt(video_description):
    """
    Generate image query prompt
    """
    prompt = f"""Given this video description, create a generic stock photo search query that would find an image that can be used as a thumbnail for the video, visually appealing image.

        IMPORTANT: Do NOT use product names, technical terms, or brand names. Instead, focus on the human element and general activity/setting that best represents the product's use.

        Video Description:
        {video_description}

        Guidelines:
        - Think about the reaction the person wants to show in the thumbnail using the video description
        - Focus on the activity being performed
        - Consider something that is catchy and can be used as a thumbnail
        - The image must be related to the video description and can easily catch attention

        Good Examples:
        Description: "I met my idol"
        ✓ "woman shocked"
        ✗ "celebrity meeting"

        Description: "How to make money online"
        ✓ "Pile of money"
        ✗ "how to work for money"

        Return ONLY three generic, stock-photo friendly words that would find a professional image of someone using/experiencing this type of product.
    """

    return prompt



def generate_vector_image_query_prompt(flyer_description):
    """
    Generate image query prompt
    """
    prompt = f"""Given this flyer description, create a generic vector image search query that would find a vector image from freepik. The vector image will be used as some of the design elements in a flyer design.
        So the search query should produce vector images that are relevant to the flyer description.

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
        ✓ "computer"
        ✗ "visual studio"

        Description: "New women's fashion store opening"
        ✓ "Gown"
        ✗ "clothing"

        Description: "Launching organic grocery delivery"
        ✓ "grocery"
        ✗ "buying"

        Return ONLY 1-2 words search query, vector image friendly words that would find a professional image of someone using/experiencing this type of product or something similar to the product settings.
    """

    return prompt

layout_types = [{"layout_name": "full_background_image", "layout_description": "For single powerful images that need full focus. In this layout there's a background image that covers the entire design, an overlay and the text is positioned strategically over the overay for visibility"}, 
                {"layout_name": "split_layout", "layout_description": "In this layout there's a split layout with the image in the right side and the content in the left side."}, 
                {"layout_name": "pattern_background", "layout_description": "This layout is a pattern background layout that uses the brands color for the pattern, an overlay and the text is positioned strategically over the overay for visibility"}, 
                {"layout_name": "card_layout", "layout_description": "A premium dark-themed card design with ambient lighting effects and a large decorative vector icon. Features a centered content card on a dark background with sophisticated lighting effects."}, 
                {"layout_name": "vector_images_design", "layout_description": "A modern, vector-enhanced layout perfect for promotional materials. Features strategic placement of thematic vector elements around clean typography, creating dynamic visual interest while maintaining professional clarity. Best suited for announcements, launches, or promotional campaigns where brand identity can be reinforced through relevant vector illustrations."}]


layout_options = {
    "full_background_image": 
        {"layout": """
            Full-Image Background Layout
    
                Implementation:
                - Full-bleed image with gradient overlay
                - Text positioned strategically over darker areas
                - The text should be on the image not under it or far right or left of it
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

        """,
        "color_mastery": """
            5. Color Mastery & Text Contrast ⚠️ CRITICAL
            RULE: Text MUST always be readable against its background

            Color Contrast Requirements:
            1. Text Over Images:
                - Light Background Image: Use dark text (#000000 or brand dark colors)
                - Dark Background Image: Use white text (#FFFFFF)
                - ALWAYS add contrast overlay behind text and make sure the text is always above the overlay:
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
                - Ensure text remains readable throughout gradient and that the text is above the gradient
                - Test contrast at lightest and darkest points
                - Add solid color block behind text if needed

            VALIDATION:
            Before generating HTML, verify:
            □ Text color contrasts with background
            □ Overlays provide sufficient contrast
            □ No text blends with background
            □ Each text element is clearly readable
            
         """,
         "content_guidelines": """
            - EVERY design MUST contain text elements:
                * Headline (Required)
                * Body text or supporting text (Required)
                * Call-to-action (Requiredif marketing idea or design guidelines requires it)
                * Social media bar (Required if the business has social media handles)
            - Content Requirements:
                * Maximum 15 words total
                * Minimum required: Headline + one other text element
                * Empty or text-free designs are FORBIDDEN
            - Text Hierarchy:
                * Headline must be most prominent
                * Supporting text must be clearly visible
                * CTA must stand out if included in the design
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

            CONTENT GRID AND DYNAMIC SIZING
            Content Zones (800px HEIGHT):
            Top Section (0-250px):
                - Logo: 30px from top, right corner, width of 80px and don't disturt the height of the logo.
                - Headlines: Start at 100px from top and make sure there's always at least 30px gap between the logo and the headline.
                - Title lines: -5px margin between
                - Headlines: Dynamic sizing based on content:
                    * For 1-3 words: 72px size
                    * For 4-6 words: 64px size
                    * For 7+ words: 56px size
                    * Never smaller than 48px
                - Each line must fit within section width
                - Auto-adjust size if lines overflow

            Middle Section (250-550px):
                - Info Box: Should have at least 80px away from the top section
                - Text treatment options:
                    * Option 1: Direct on gradient overlay (preferred)
                    * Option 2: If needed, subtle text-shadow for contrast
                - NO semi-transparent boxes around text
                - NO container boxes for body text
                - Content must stay within vertical bounds
                - Spacing adjusts based on content volume
                - Content must not overflow section
                - Make sure the content stays between 250px and 550px and reduce the font size if it overflows.

                ❌ FORBIDDEN:
                - Body text extending into CTA zone
                - Inadequate spacing between content blocks
                - Missing gaps between sections
                - Flexible/auto margins between content
                - Semi-transparent boxes around body text
                - Container boxes around descriptive text
                - Text blocks with visible backgrounds
                - Boxing/containing regular text content

                ✅ REQUIRED:
                - Fixed 60px gap before bottom section
                - Explicit flex-direction and gap values
                - Clear separation between content blocks
                - Proper use of margin-bottom/margin-top

                

            Bottom Section (550-800px):
                - Social Bar: Fixed 40px from bottom
                - Maintains position regardless of content above
                - Must be implemented if any social handles exist
                - Structure Requirements:
                    * Font Awesome icons for all available platforms
                    * Icons MUST contrast with background
                    * Size: 24px for all icons
                    * Spacing: 20px gap between icons
                    * Handle text after icons
                    * 1px line above (rgba(255,255,255,0.2))

                Bottom Elements Placement Rules:
                1. CTA Button (if marketing idea or design guidelines requires it):
                    - Position above social media
                    - Full width of content area
                    - Background color matching brand
                    - 24px gap below button

                2. Social Media Bar:
                    - Always at very bottom
                    - Align left within content area
                    - Maintain consistent height (40px)
                    - No overlapping with CTA
                    - Single line implementation

                ❌ FORBIDDEN:
                    - Social media overlapping CTA
                    - Stacked social icons
                    - Multi-line social handles
                    - CTA button too close to body text
                    - Floating/unanchored social bar
                    - Social icons overlapping button text
                    - Button background touching social bar
                    - Stacked interactive elements
                    - Social bar sandwiched between other elements

                ✅ REQUIRED:
                    - Fixed bottom positioning for social
                    - Clear separation from main content
                    - Single-line social bar
                    - Full-width CTA button
                    - Proper vertical spacing
                    - 60px minimum between CTA and social bar
                    - 40px clear space around social bar
                    - Distinct zones for CTA and social elements
                    - Full padding around button text

         """,
         "usage_and_description": "For single powerful images that need full focus. In this layout there's a background image that covers the entire design, an overlay and the text is positioned strategically over the overay for visibility"},
        "split_layout": 
        {"layout": """
            Split Layout
    
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

            Content Organization in Split Space:
            .content-area {{     
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                height: 100%;
            }}

            .main-content {{
                flex: 1;
                display: flex;
                flex-direction: column;
                gap: 30px;
            }}

            .bottom-elements {{
                margin-top: auto;
                display: flex;
                flex-direction: column;
                gap: 24px;
            }}

            Bottom Elements Placement Rules:
            1. CTA Button:
                - Position above social media
                - Full width of content area
                - Background color matching brand
                - 24px gap below button

            2. Social Media Bar:
                - Always at very bottom
                - Align left within content area
                - Maintain consistent height (40px)
                - No overlapping with CTA
                - Single line implementation

            ❌ FORBIDDEN IN SPLIT LAYOUT:
                - Social media overlapping CTA
                - Stacked social icons
                - Multi-line social handles
                - CTA button too close to body text
                - Floating/unanchored social bar

            ✅ REQUIRED IN SPLIT LAYOUT:
                - Fixed bottom positioning for social
                - Clear separation from main content
                - Single-line social bar
                - Full-width CTA button
                - Proper vertical spacing

        """,
        "color_mastery": """
            5. Color Mastery & Text Contrast ⚠️ CRITICAL
            RULE: Text MUST always be readable against its background

            Color Contrast Requirements:
            1. Text Over Solid Colors:
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
                - Ensure text remains readable throughout gradient and that the text is above the gradient
                - Test contrast at lightest and darkest points
                - Add solid color block behind text if needed

            VALIDATION:
            Before generating HTML, verify:
            □ Text color contrasts with background
            □ Overlays provide sufficient contrast
            □ No text blends with background
            □ Each text element is clearly readable
            
         """,
         "content_guidelines": """
            - EVERY design MUST contain text elements:
                * Headline (Required)
                * Body text or supporting text (Required)
                * Call-to-action (Requiredif marketing idea or design guidelines requires it)
                * Social media bar (Required if the business has social media handles)
            - Content Requirements:
                * Maximum 15 words total
                * Minimum required: Headline + one other text element
                * Empty or text-free designs are FORBIDDEN
            - Text Hierarchy:
                * Headline must be most prominent
                * Supporting text must be clearly visible
                * CTA must stand out if included in the design
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

            CONTENT GRID AND DYNAMIC SIZING
            Content Zones (800px HEIGHT):
            Top Section (0-250px):
                - Logo: 30px from top, right corner, width of 80px and don't disturt the height of the logo.
                - Headlines: Start at 100px from top and make sure there's always at least 30px gap between the logo and the headline.
                - Title lines: -5px margin between
                - Headlines: Dynamic sizing based on content:
                    * For 1-3 words: 72px size
                    * For 4-6 words: 64px size
                    * For 7+ words: 56px size
                    * Never smaller than 48px
                - Each line must fit within section width
                - Auto-adjust size if lines overflow

            Middle Section (250-550px):
                - Info Box: Should have at least 80px away from the top section
                - Text treatment options:
                    * Option 1: Direct on gradient overlay (preferred)
                    * Option 2: If needed, subtle text-shadow for contrast
                - NO semi-transparent boxes around text
                - NO container boxes for body text
                - Content must stay within vertical bounds
                - Spacing adjusts based on content volume
                - Content must not overflow section
                - Make sure the content stays between 250px and 550px and reduce the font size if it overflows.

                ❌ FORBIDDEN:
                - Body text extending into CTA zone
                - Inadequate spacing between content blocks
                - Missing gaps between sections
                - Flexible/auto margins between content
                - Semi-transparent boxes around body text
                - Container boxes around descriptive text
                - Text blocks with visible backgrounds
                - Boxing/containing regular text content

                ✅ REQUIRED:
                - Fixed 60px gap before bottom section
                - Fixed 40px gap between the call to action and the social bar
                - Explicit flex-direction and gap values
                - Clear separation between content blocks
                - Proper use of margin-bottom/margin-top

                

            Bottom Section (550-800px):
                - Social Bar: Fixed 40px from bottom
                - Maintains position regardless of content above
                - Must be implemented if any social handles exist
                - Structure Requirements:
                    * Font Awesome icons for all available platforms
                    * Icons MUST contrast with background
                    * Size: 24px for all icons
                    * Spacing: 20px gap between icons
                    * Handle text after icons
                    * 1px line above (rgba(255,255,255,0.2))

                Bottom Elements Placement Rules:
                1. CTA Button (if marketing idea or design guidelines requires it):
                    - Position above social media
                    - Full width of content area
                    - Background color matching brand
                    - 24px gap below button

                2. Social Media Bar:
                    - Always at very bottom
                    - Align left within content area
                    - Maintain consistent height (40px)
                    - No overlapping with CTA
                    - Single line implementation

                ❌ FORBIDDEN:
                    - Social media overlapping CTA
                    - Stacked social icons
                    - Multi-line social handles
                    - CTA button too close to body text
                    - Floating/unanchored social bar
                    - Social icons overlapping button text
                    - Button background touching social bar
                    - Stacked interactive elements
                    - Social bar sandwiched between other elements

                ✅ REQUIRED:
                    - Fixed bottom positioning for social
                    - Clear separation from main content
                    - Single-line social bar
                    - Full-width CTA button
                    - Proper vertical spacing
                    - 40px minimum between CTA and social bar
                    - 40px clear space around social bar
                    - Distinct zones for CTA and social elements
                    - Full padding around button text

         """,
         "usage_and_description": "In this layout there's a split layout with the image in the right side and the content in the left side."},
        
        "pattern_background": 
        {"layout": """
            Pattern Background Layout
    
            1. CONTAINER STRUCTURE
                Main Container:
                - Dimensions: 800px × 800px
                - Primary brand color background
                - Drop shadow: 0 20px 40px rgba(0,0,0,0.2)
                - There's no need to put an image in the background for this layout style.

                Pattern Requirements:
                - Diagonal stripes MUST be exact:
                    * Darker shade of primary color
                    * Angle: -45 degrees
                    * Width: 40px (20px color + 20px gap)
                    * Opacity: 100% (fully opaque)
                    * Pattern must be subtle, not competing

            2. LAYER STACKING
                Base Container: z-index: 1
                Pattern Background: z-index: 2 (absolute positioned)
                Content Wrapper: z-index: 10 (relative positioned)

            3. CONTENT GRID AND DYNAMIC SIZING
                Content Zones (800px HEIGHT):
                Top Section (0-250px):
                    - Logo: 30px from top, right corner, width of 80px and don't disturt the height of the logo.
                    - Headlines: Start at 100px from top and make sure there's always at least 30px gap between the logo and the headline.
                    - Title lines: -5px margin between
                    - Headlines: Dynamic sizing based on content:
                        * For 1-3 words: 72px size
                        * For 4-6 words: 64px size
                        * For 7+ words: 56px size
                        * Never smaller than 48px
                    - Each line must fit within section width
                    - Auto-adjust size if lines overflow

                Middle Section (250-550px):
                    - Info Box: Should have at least 80px away from the top section
                    - Spacing adjusts based on content volume
                    - Content must not overflow section
                    - Make sure the content stays between 250px and 550px and reduce the font size if it overflows.

                Bottom Section (550-800px):
                    - Social Bar: Fixed 40px from bottom
                    - Maintains position regardless of content above
                    - Must be implemented if any social handles exist
                    - Structure Requirements:
                        * Font Awesome icons for all available platforms
                        * Icons MUST contrast with background
                        * Size: 24px for all icons
                        * Spacing: 20px gap between icons
                        * Handle text after icons
                        * 1px line above (rgba(255,255,255,0.2))

                    Bottom Elements Placement Rules:
                    1. CTA Button (if marketing idea or design guidelines requires it):
                        - Position above social media
                        - Full width of content area
                        - Background color matching brand
                        - 24px gap below button

                    2. Social Media Bar:
                        - Always at very bottom
                        - Align left within content area
                        - Maintain consistent height (40px)
                        - No overlapping with CTA
                        - Single line implementation

                    ❌ FORBIDDEN:
                        - Social media overlapping CTA
                        - Stacked social icons
                        - Multi-line social handles
                        - CTA button too close to body text
                        - Floating/unanchored social bar
                        - Social icons overlapping button text
                        - Button background touching social bar
                        - Stacked interactive elements
                        - Social bar sandwiched between other elements

                    ✅ REQUIRED:
                        - Fixed bottom positioning for social
                        - Clear separation from main content
                        - Single-line social bar
                        - Full-width CTA button
                        - Proper vertical spacing
                        - 60px minimum between CTA and social bar
                        - 40px clear space around social bar
                        - Distinct zones for CTA and social elements
                        - Full padding around button text

            4. TYPOGRAPHY AND TEXT PLACEMENT
                Dynamic Text Sizing:
                Headlines:
                - Base size: 72px
                - Adjustment rules:
                    * If text width > 80% container: Reduce by 8px
                    * If lines overlap: Reduce by 4px
                    * Continue reducing until no overlap
                    * Minimum size: 48px
                - Weight: Bold (700)
                - Line height: -2px
                - Maximum 3 lines
                - CRITICAL: Highlighted text MUST be separate from other elements
                
                Title Line Rules:
                - Check width of each line
                - Maintain consistent size across lines
                - Adjust all lines if any needs resizing


                Highlight Box Rules:
                - Must have its own dedicated space
                - NO overlapping with other text elements
                - When used with dates/location:
                    * Date/location must be BELOW or ABOVE highlight box
                    * Minimum 20px spacing from highlight box
                    * Never inside or overlapping highlight box
                
                Text Separation Rules:
                - Each text element needs clear space
                - Minimum spacing between elements:
                    * Between title lines: -5px (intentional overlap)
                    * Between title and highlight: 20px
                    * Between highlight and info: 30px
                    * Between info and CTA: 40px
                
                
                ❌ ADDITIONAL FORBIDDEN:
                - Text elements should never overlap each other in the whole design
                - Info text inside highlight boxes
                - Multiple elements in same highlight box
                - Stacked text without proper spacing

                Layout Validation:
                    Before rendering:
                    □ Calculate total text width
                    □ Verify space requirements
                    □ Adjust font sizes if needed
                    □ Confirm no overlaps

            5. CRITICAL CSS
                .container {{
                    position: relative;
                    background: var(--primary-color);
                    overflow: hidden;
                }}
                .pattern-background {{
                    position: absolute;
                    inset: 0;
                    background: repeating-linear-gradient(
                        -45deg,
                        var(--primary-dark) 0px,
                        var(--primary-dark) 20px,
                        transparent 20px,
                        transparent 40px
                    );
                }}
                

            ✅ REQUIRED:
            - Exact vertical space distribution
            - Left-aligned content
            - One highlighted word/phrase
            - Social bar with icons AND handle
            - Content fills 80% of vertical space
            - Text MUST be above pattern
            - Designs must have a social bar
            - Top section should be in the top 30% of the design, middle section should be in the middle 40% of the design and the bottom section should be in the bottom 30% of the design. Each section have their own dedicated space and never cross each other.
            - Each section should be at least 30px away from each other vertically.

            ❌ FORBIDDEN:
            - Empty bottom section
            - Missing social media elements
            - Text under pattern layer
            - Centered alignments
            - Unbalanced vertical spacing
            - Small text sizes
            - Designs that don't have a social bar
            - Sections that don't have their own dedicated space or cross each other

        """,
        "color_mastery": """
            5. Color Mastery & Text Contrast ⚠️ CRITICAL
            RULE: Text MUST always be readable against its background

            Color Contrast Requirements:
            1. Text Over Images:
                - Light Background Image: Use dark text (#000000 or brand dark colors)
                - Dark Background Image: Use white text (#FFFFFF)
                - ALWAYS add contrast overlay behind text and make sure the text is always above the overlay:
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
                - Ensure text remains readable throughout gradient and that the text is above the gradient
                - Test contrast at lightest and darkest points
                - Add solid color block behind text if needed

            VALIDATION:
            Before generating HTML, verify:
            □ Text color contrasts with background
            □ Overlays provide sufficient contrast
            □ No text blends with background
            □ Each text element is clearly readable
            
         """,
         "content_guidelines": """
            - EVERY design MUST contain text elements:
                * Headline (Required)
                * Body text or supporting text (Required)
                * Call-to-action (Requiredif marketing idea or design guidelines requires it)
                * Social media bar (Required if the business has social media handles)
            - Content Requirements:
                * Maximum 15 words total
                * Minimum required: Headline + one other text element
                * Empty or text-free designs are FORBIDDEN
            - Text Hierarchy:
                * Headline must be most prominent
                * Supporting text must be clearly visible
                * CTA must stand out if included in the design
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

            CONTENT GRID AND DYNAMIC SIZING
            Content Zones (800px HEIGHT):
            Top Section (0-250px):
                - Logo: 30px from top, right corner, width of 80px and don't disturt the height of the logo.
                - Headlines: Start at 100px from top and make sure there's always at least 30px gap between the logo and the headline.
                - Title lines: -5px margin between
                - Headlines: Dynamic sizing based on content:
                    * For 1-3 words: 72px size
                    * For 4-6 words: 64px size
                    * For 7+ words: 56px size
                    * Never smaller than 48px
                - Each line must fit within section width
                - Auto-adjust size if lines overflow

            Middle Section (250-550px):
                - Info Box: Should have at least 80px away from the top section
                - Text treatment options:
                    * Option 1: Direct on gradient overlay (preferred)
                    * Option 2: If needed, subtle text-shadow for contrast
                - NO semi-transparent boxes around text
                - NO container boxes for body text
                - Content must stay within vertical bounds
                - Spacing adjusts based on content volume
                - Content must not overflow section
                - Make sure the content stays between 250px and 550px and reduce the font size if it overflows.

                ❌ FORBIDDEN:
                - Body text extending into CTA zone
                - Inadequate spacing between content blocks
                - Missing gaps between sections
                - Flexible/auto margins between content
                - Semi-transparent boxes around body text
                - Container boxes around descriptive text
                - Text blocks with visible backgrounds
                - Boxing/containing regular text content

                ✅ REQUIRED:
                - Fixed 60px gap before bottom section
                - Explicit flex-direction and gap values
                - Clear separation between content blocks
                - Proper use of margin-bottom/margin-top

                

            Bottom Section (550-800px):
                - Social Bar: Fixed 40px from bottom
                - Maintains position regardless of content above
                - Must be implemented if any social handles exist
                - Structure Requirements:
                    * Font Awesome icons for all available platforms
                    * Icons MUST contrast with background
                    * Size: 24px for all icons
                    * Spacing: 20px gap between icons
                    * Handle text after icons
                    * 1px line above (rgba(255,255,255,0.2))

                Bottom Elements Placement Rules:
                1. CTA Button (if marketing idea or design guidelines requires it):
                    - Position above social media
                    - Full width of content area
                    - Background color matching brand
                    - 24px gap below button

                2. Social Media Bar:
                    - Always at very bottom
                    - Align left within content area
                    - Maintain consistent height (40px)
                    - No overlapping with CTA
                    - Single line implementation

                ❌ FORBIDDEN:
                    - Social media overlapping CTA
                    - Stacked social icons
                    - Multi-line social handles
                    - CTA button too close to body text
                    - Floating/unanchored social bar
                    - Social icons overlapping button text
                    - Button background touching social bar
                    - Stacked interactive elements
                    - Social bar sandwiched between other elements

                ✅ REQUIRED:
                    - Fixed bottom positioning for social
                    - Clear separation from main content
                    - Single-line social bar
                    - Full-width CTA button
                    - Proper vertical spacing
                    - 60px minimum between CTA and social bar
                    - 40px clear space around social bar
                    - Distinct zones for CTA and social elements
                    - Full padding around button text

         """,
         "usage_and_description": "This layout is a pattern background layout that uses the brands color for the pattern, an overlay and the text is positioned strategically over the overay for visibility."},

    "card_layout": {
    "layout": """
        Dark Card Design Layout

        STRUCTURE:
        body {
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: radial-gradient(circle at center, #1d1d1d 0%, #000000 100%);
            margin: 0;
            overflow: hidden;
        }

        .card-container {
            width: 800px;
            height: 800px;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        Background Elements:
        .ambient-light {
            position: absolute;
            inset: 0;
            background: radial-gradient(
                circle at 70% 30%,
                rgba(var(--brand-rgb), 0.15),
                transparent 70%
            );
            pointer-events: none;
        }

        Content Card:
        .content-card {
            width: 600px;
            height: 400px;
            background: rgba(var(--brand-rgb), 0.9);
            border-radius: 30px;
            padding: 40px;
            position: relative;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }

        CRITICAL RULES:
        1. Body MUST:
            - Use height: 100vh (not min-height)
            - Have margin: 0
            - Set overflow: hidden
            - Use flexbox for centering
        
        2. Container MUST:
            - Maintain 800x800 dimensions
            - Use flexbox for centering
            - No padding or margins
        
        3. Ambient Light MUST:
            - Use inset: 0 instead of width/height
            - Remain fixed in container
        
        ❌ FORBIDDEN:
        - Using min-height on body
        - Adding padding to body
        - Using viewport units for container
        - Setting overflow on container
        
        ✅ REQUIRED:
        - Fixed body height
        - Hidden overflow
        - Zero body margins
        - Proper flexbox centering

        4. Vector Icon Requirements:
            - Use FontAwesome icon relevant to brand
            - Position: Bottom right, partially off-card
            - Size: 240px (font-size)
            - Color: rgba(255,255,255,0.1)
            - Transform: rotate(-15deg)

        5. Social Media Bar:
            - Position: Bottom of content card
            - Background: rgba(0,0,0,0.2)
            - Border-radius: 15px
            - Padding: 10px 20px
            - Icons: white with 0.9 opacity
            - Handle: white text, 16px size

        ❌ FORBIDDEN:
        - White/light backgrounds
        - Multiple decorative icons
        - Centered text alignment
        - Sharp corners
        - Solid color backgrounds
        
        ✅ REQUIRED:
        - Radial gradient background
        - Single large vector icon
        - Left-aligned text
        - Rounded corners
        - Ambient lighting effect
    """,

    "color_mastery": """
        Color Requirements:
        1. Background:
            - Dark radial gradient
            - Center: #1d1d1d
            - Edges: #000000
        
        2. Content Card:
            - Use brand color with 0.9 opacity
            - Text: White (#ffffff)
            - Highlight pill: White background, dark text
        
        3. Icon and Elements:
            - Decorative icon: rgba(255,255,255,0.1)
            - CTA button: Black background, white text
            - Social icons: White with 0.9 opacity
        
        4. Ambient Light:
            - Use brand color with 0.15 opacity
            - Radial gradient from top right
            - Fade to transparent
    """,

    "content_guidelines": """
        Text Layout:
        1. Headline:
            - Size: 48px
            - Weight: Bold (700)
            - Color: White
            - Include highlight pill word
            - Maximum 8 words
        
        2. Subtext:
            - Size: 18px
            - Weight: Regular
            - Color: White
            - Maximum 20 words
            - Width: 400px max
        
        3. CTA Button:
            - Size: 18px
            - Weight: Semibold (600)
            - Black background
            - White text
            - Padding: 15px 30px
            - Hover: translateY(-2px)
        
        4. Social Media Bar:
            - Position: Bottom of card
            - Icon size: 18px
            - Handle text: 16px
            - Spacing: 15px between icons

            Social Media Bar Placement:
            1. Fixed Position Rules:
                - MUST be at bottom of content card
                - 30px minimum from bottom edge
                - Clear separation from main content (40px gap)
                - Never overlap with other text elements
                
            2. Social Bar Structure:
                Layout:
                .social-media-bar {
                    position: absolute;
                    bottom: 30px;
                    left: 40px;
                    right: 40px;
                    display: flex;
                    align-items: center;
                    gap: 15px;
                    padding: 12px 20px;
                    background: rgba(255,255,255,0.1);
                    border-radius: 12px;
                }

                Icons Section:
                .social-icons {
                    display: flex;
                    gap: 15px;
                    align-items: center;
                }

                Handle Text:
                .social-handle {
                    margin-left: auto;
                    font-size: 16px;
                    color: rgba(255,255,255,0.9);
                }

            3. Critical Rules:
                ❌ FORBIDDEN:
                - Placing social bar over main content
                - Stacking social icons vertically
                - Multiple rows of social handles
                - Overlapping with CTA button
                - Social bar in middle of content

                ✅ REQUIRED:
                - Fixed bottom positioning
                - Single line implementation
                - Semi-transparent background
                - Clear spacing from content above
                - All icons same size (20px)

            4. Content Safe Zone:
                - Main content must end 100px above card bottom
                - Maintain 40px minimum gap above social bar
                - No text elements in bottom 80px except social bar
                - If CTA exists, place 60px above social bar

        Content Spacing:
        - Logo: 20px from top and right edges
        - Headline: 40px from top
        - Subtext: 20px below headline
        - CTA: 30px below subtext
        - Social bar: 30px from bottom
    """,

    "usage_and_description": "A premium dark-themed card design with ambient lighting effects and a large decorative vector icon. Perfect for announcements, launches, or premium offerings. Features a centered content card on a dark background with sophisticated lighting effects."
    },
    "vector_images_design":
    {
    "layout": """
        Modern Vector-Based Layout

        STRUCTURE:
        .container {
            width: 800px;
            height: 800px;
            background: var(--brand-color);
            position: relative;
            padding: 60px;
            overflow: hidden;
        }

        Content Area:
        .content {
            position: relative;
            z-index: 2;
            max-width: 500px;
            margin-top: 80px;
        }

        Vector Elements:
        .vector-element {
            position: absolute;
            filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.15));
        }

        VECTOR PLACEMENT & TEXT RELATIONSHIP:
        1. Vector Safe Zones:
            - Primary: Empty spaces with no text
            - Minimum 40px clearance from any text
        
        2. Text Priority Rules:
            - Text always takes precedence over vectors
            - Vectors must not interfere with readability
            - Vector should not overlap text, vector should be in clear spaces without text
            - Text must remain on clear background area
        
        3. Vector Z-Index Management:
            .text-content {
                z-index: 2;
                position: relative;
            }
            .vector-element {
                z-index: 1;
            }
            .vector-element.behind-text {
                z-index: 0;
                opacity: 0.8;
            }

        4. Space Management:
            - Map out text areas first
            - Place vectors in remaining spaces
            - Maintain clear visual hierarchy
            - Create intentional white space
        
        ❌ FORBIDDEN:
            - Vectors overlapping text at same z-index
            - Vectors in primary reading areas
            - Dense vector placement near text
            - Vectors that reduce text contrast
            - Vector overlapping, under or on top of text
            - Vector overlapping, under or on top of other vectors
            - Vector overlapping, under or on top of the logo
            - Vector overlapping, under or on top of the CTA button
            - Vector overlapping, under or on top of the social media bar
            
        ✅ REQUIRED:
            - Clear text priority
            - Strategic vector placement
            - Proper layering when needed
            - Maintain text readability
            
        Vector Placement Validation:
        □ Check all text areas are clear
        □ Verify vector-text separation
        □ Confirm z-index hierarchy
        □ Test readability with vectors

        CRITICAL RULES:
        1. Vector Placement:
            - Don't us more than 3 vectors
            - The vectors should be between 60px and 140px in size
            - Don't place the vectors under or ontop of a text, call to action, logo or social media bar
            - Vectors can be placed in free floating spaces without text, call to action, logo or social media bar
            
        2. Vector Styling:
            - Must use provided vector_assets
            - Apply drop-shadow for depth
            - Rotate for dynamic feel (-15 to 15 degrees)
            - Scale based on position (larger at edges)
            
        3. Layout Balance:
            - Never crowd the content area
            - Space vectors evenly
            - Maintain clear hierarchy
            - Ensure vectors complement text
        
        4. Background:
            - The background should be a dark color, the color should be the brand color
            - Don't use image background for this design
            - Since the background is a dark solid color don't put an overlay on the background

        ❌ FORBIDDEN:
            - Overlapping vectors with text
            - Too many vectors (max 3)
            - Vectors too close together
            - Excessive rotation (>25deg)
            - Background that is an image or has an overlay
            
        ✅ REQUIRED:
            - Strategic vector placement
            - Consistent size ratios
            - Clear content space
            - Dynamic composition
            - Proper z-indexing
            - Background is a dark color, the color should be the brand color
            - Don't use image background for this design
            - Since the background is a dark solid color don't put an overlay on the background
    """,

    "color_mastery": """
        Color Requirements:
        1. Background:
            - Use brand color at 100%
            - Keep background clean and solid
            - Don't use image background for this design
        
        2. Vector Colors:
            - Maintain original vector colors
            - Ensure contrast with background
            - Use drop-shadow for depth
    """,

    "content_guidelines": """    
        CONTENT GRID AND DYNAMIC SIZING

        The design must not have more than 25 words in the content.
        Content Zones (800px HEIGHT):
        Top Section (0-250px):
            - Logo: 30px from top, right corner, width of 80px and don't disturt the height of the logo.
            - Headlines: Start at 100px from top and make sure there's always at least 30px gap between the logo and the headline.
            - Title lines: -5px margin between
            - Headlines: Dynamic sizing based on content:
                * For 1-3 words: 72px size
                * For 4-6 words: 64px size
                * For 7+ words: 56px size
                * Never smaller than 48px
            - Each line must fit within section width
            - Auto-adjust size if lines overflow

        Middle Section (250-550px):
            - Info Box: Should have at least 80px away from the top section
            - Text treatment options:
                * Option 1: Direct on gradient overlay (preferred)
                * Option 2: If needed, subtle text-shadow for contrast
            - NO semi-transparent boxes around text
            - NO container boxes for body text
            - Content must stay within vertical bounds
            - Spacing adjusts based on content volume
            - Content must not overflow section
            - Make sure the content stays between 250px and 550px and reduce the font size if it overflows.

            ❌ FORBIDDEN:
            - Body text extending into CTA zone
            - Inadequate spacing between content blocks
            - Missing gaps between sections
            - Flexible/auto margins between content
            - Semi-transparent boxes around body text
            - Container boxes around descriptive text
            - Text blocks with visible backgrounds
            - Boxing/containing regular text content

            ✅ REQUIRED:
            - Fixed 60px gap before bottom section
            - Fixed 40px gap between the call to action and the social bar
            - Explicit flex-direction and gap values
            - Clear separation between content blocks
            - Proper use of margin-bottom/margin-top

            

        Bottom Section (550-800px):
            - Social Bar: Fixed 40px from bottom
            - Maintains position regardless of content above
            - Must be implemented if any social handles exist
            - Structure Requirements:
                * Font Awesome icons for all available platforms
                * Icons MUST contrast with background
                * Size: 24px for all icons
                * Spacing: 20px gap between icons
                * Handle text after icons
                * 1px line above (rgba(255,255,255,0.2))

            Bottom Elements Placement Rules:
            1. CTA Button (if marketing idea or design guidelines requires it):
                - Position above social media
                - Full width of content area
                - Background color matching brand
                - 24px gap below button

            2. Social Media Bar:
                - Always at very bottom
                - Align left within content area
                - Maintain consistent height (40px)
                - No overlapping with CTA
                - Single line implementation

            ❌ FORBIDDEN:
                - Social media overlapping CTA
                - Stacked social icons
                - Multi-line social handles
                - CTA button too close to body text
                - Floating/unanchored social bar
                - Social icons overlapping button text
                - Button background touching social bar
                - Stacked interactive elements
                - Social bar sandwiched between other elements
                - A design without a social media bar

            ✅ REQUIRED:
                - Fixed bottom positioning for social
                - Clear separation from main content
                - Single-line social bar
                - Full-width CTA button
                - Proper vertical spacing
                - 40px minimum between CTA and social bar
                - 40px clear space around social bar
                - Distinct zones for CTA and social elements
                - Full padding around button text

    """,
    
    "usage_and_description": "A modern, vector-enhanced layout perfect for promotional materials. Features strategic placement of thematic vector elements around clean typography, creating dynamic visual interest while maintaining professional clarity. Best suited for announcements, launches, or promotional campaigns where brand identity can be reinforced through relevant vector illustrations."
    }
}

def generate_initial_design_prompt(business_details, image_url, other_images, layout_option, vector_images = None):
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
        - If the layout style is the vector images design, you must use the vector images provided: {vector_images}


    4. CRITICAL: Logo Handling & Sizing ⚠️
        RULES:
        1. Logo Size Requirements:
            - Maximum logo size: 100px width
            - Minimum logo size: 80px width
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
            - Social media section MUST include:
                * All platform icons (Facebook, Instagram, Twitter, TikTok)
                * Handle text (e.g., "@nba")
                * Horizontal line above
                * Proper spacing and alignment
        
        VALIDATION:
        Before generating HTML:
        □ Check logo dimensions
        □ Verify corner placement
        □ Confirm logo doesn't dominate
        □ Ensure NO text in logo zone
        □ Verify text starts outside logo area
        □ Test visual hierarchy balance
        □ Check 120px × 120px corner is clear for logo

    
    {layout_option["color_mastery"]}

    6. Professional Refinements
        - Use modern border-radius (30px for call to actions)
        - Maintain consistent spacing rhythm

    7. Content Guidelines ⚠️ MANDATORY TEXT CONTENT
        You have been provided with a sample image of the implementation of the layout, use it as well to understand the layout better and design a better flyer.
        This examples have been designed by our team or generated by our AI during training previously and we consider them good examples for you to learn from without any copyright infringement.

        {layout_option["content_guidelines"]}

    
    8. LAYOUT ⚠️ CRITICAL
        {layout_option["layout"]}

    9. Container Styling & Space Distribution ⚠️
        DIMENSIONS:
        - Main container: 800px × 800px
        - Maintain consistent 40px padding
        - Never put this main container in another container or body, the main container is the entire design.
        
        CONTENT DISTRIBUTION RULES:
        1. Vertical Space Division:
            - Top Section (30%): Logo and headline
            - Middle Section (40%): Main content
            - Bottom Section (30%): CTA and social media
        
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
        - professional looking call to action
        - Smooth color transitions
        - Elegant scaling effects
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
                <i class="fab fa-square-x-twitter"></i>
                <i class="fab fa-tiktok"></i>
                <i class="fab fa-youtube"></i>
                <i class="fab fa-linkedin"></i>
                <i class="fab fa-pinterest"></i>
                
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
        - Make sure the icons and the handle text are in the same row.
        - Make sure the icons and the handle text are in a color that contrasts with the background, so it's visible. The icons and the handle text should also be in thesame color. 
        ❌ WRONG: Just icons without handle text
        ✅ RIGHT: Icons + "@starbucks"

        Social Media Implementation Rules:
        1. Icons Placement:
            - Single instance of each icon
            - No duplicate icons
            - Horizontal alignment only
            
        ❌ FORBIDDEN:
            - Duplicate social media icons
            - Multiple rows of icons
            - Repeated platform icons
            - Icons after handle text
            - Missing social media section
            - Icons without handle
            - Handle without icons
            - Incorrect icon order

        ✅ REQUIRED:
            - Single row of unique icons
            - One handle for all icons
            - Icons grouped together
            - Icons before handle text
            - If all the social media handles provided are thesame for all social media, you can have all the icons side by side and the handle text after the icons. Use the format: icon1 icon2 icon3 @handle
            - If the social media handles provided are different for some social media, use the format: icon + handle text

    12. Call to Action
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
    - Animations: No animations its a static flyer design
    - Borders: Modern radius (20-30px)
    - Clearity: Never place overlays or gradients ontop of texts or else they won't be visible

    OUTPUT: Generate only valid HTML/CSS code, no explanations.
    """
    return prompt


def generate_refine_design_prompt(feedback):
    """Generate the refine design prompt"""
    prompt = f"""Modify the previous HTML/CSS flyer design based on this feedback while maintaining all design principles and quality.

        IMPORTANT FEEDBACK HANDLING RULES:

        1. Previous Request Context:
            - Review the complete conversation history
            - Check if this feedback relates to previous requests
            - If similar feedback was given before, prioritize fixing it completely

        2. Social Media Implementation:
            - Always implement social icons using FontAwesome
            - Icons MUST be inline with handle text
            - Single instance of each platform icon
            - Required format: [fb][tw][ig] @handle
            - NO duplicate icons allowed
            
            Example:
            <div class="social-media-bar">
                <div class="social-icons">
                    <i class="fab fa-facebook"></i>
                    <i class="fab fa-instagram"></i>
                    <i class="fab fa-twitter"></i>
                    <i class="fab fa-tiktok"></i>
                </div>
                <span class="social-handle">@handle</span>
            </div>

            ❌ FORBIDDEN:
            - Multiple instances of same icon
            - Icons appearing after handle
            - Platform icons repeated
            - Scattered icon placement
            - Individual handles for each icon

        3. Spacing Adjustments:
            - When moving elements, use explicit pixel values
            - Ensure no overlap after adjustments
            - Validate new positions don't create new conflicts
            
            SPACING ADJUSTMENT INTELLIGENCE:
            1. Understanding Spacing Feedback:
                - "closer" = reduce current spacing
                - "farther/further" = increase current spacing
                - "much closer" = significant reduction
                - "slightly closer" = minor reduction
                - "too much space" = excessive gap needs reduction
                - "too tight" = insufficient gap needs increase
                
            2. Proportional Adjustments:
                For moving elements:
                - Analyze current gap between elements
                - Determine adjustment direction (closer/farther)
                - Apply proportional changes:
                    * Standard move: Adjust by 40% of current gap
                    * Slight move: Adjust by 20% of current gap
                    * Major move: Adjust by 60% of current gap
                - Never reduce gaps below 4px minimum
                - Never increase gaps beyond 40px maximum
            
            3. Context-Aware Spacing:
                - Consider element relationships:
                    * Related text elements (like "Appstore @handle")
                    * Navigation items
                    * Icon groups
                    * Content sections
                - Maintain visual hierarchy
                - Preserve design balance
                
            4. Validation Rules:
                Before implementing spacing changes:
                □ Identify affected elements
                □ Measure current spacing
                □ Determine appropriate adjustment ratio
                □ Check minimum/maximum constraints
                □ Verify visual relationships maintained
                □ Test readability/clarity
                □ Ensure no overlap created

        4. Critical Validation Before Output:
            □ Verify the specific change requested is implemented
            □ Check no new spacing issues were created
            □ Confirm social media elements are properly formatted
            □ Ensure CTA and social media maintain proper separation
            □ Validate all previous design principles are maintained

        Current Feedback to Implement:
        {feedback}

        ❌ FORBIDDEN:
        - Partial implementation of feedback
        - Creating new spacing issues
        - Overlapping elements
        - Missing social media icons
        - Incomplete changes

        ✅ REQUIRED:
        - Complete implementation of feedback
        - Proper spacing maintenance
        - Correct social media formatting
        - Clean element separation
        - Retention of design quality

        Return only the complete, updated HTML code.
        """
    
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


thumbnail_layout_options = {
    "tiktok_thumbnail_layout_1": {
        "layout_size": "1080px × 1920px",
        "layout": """
            TikTok Thumbnail Layout
            
            1. CONTAINER STRUCTURE
                - Dimensions: 1080px × 1920px
                - Background: Video screenshot/image
                - NO overlays or gradients (clear visibility required)
                
            2. TEXT HIERARCHY
                Main Text:
                - Font: Inter Black or similar
                - Size: 72-84px for short text, scale down for longer
                - Weight: 800-900
                - Color: White with black shadow
                - Position: 65-70% from top
                
                Highlight Text (Optional):
                - Background: Solid bright color (#FF0040 recommended)
                - Padding: 8px 20px
                - Rotation: -2deg
                - Box Shadow: 4px 4px rgba(0,0,0,0.3)
                
            3. EMOJI PLACEMENT
                - Inline Emojis: Same size as text
                - Text Emojis: After or between words
            
                
                
            ❌ FORBIDDEN:
            - Centered text alignments for long phrases
            - More than 3 lines of text
            - Small or unreadable text
            - Emoji overload (max 4 total)
            - Any overlays or gradients
            
            ✅ REQUIRED:
            - High contrast text
            - Strategic emoji placement
            - Clear hierarchy
            - Gen-Z friendly styling
            - Proper spacing around elements
            - Full clear background image without overlays or gradients
        """,
        "usage_and_description": "TikTok thumbnail layout optimized for maximum engagement and readability, featuring bold text and strategic emoji placement."
    },
    "tiktok_thumbnail_layout_2": {
        "layout_size": "1080px × 1920px",
        "layout": """
            Social Story Thumbnail Layout
            
            1. CONTAINER STRUCTURE
                - Dimensions: 1080px × 1920px
                - Background: Full video screenshot/image
                - NO overlays or gradients (clear visibility required)
                
            2. TEXT HIERARCHY
                Main Text:
                - Font: Poppins Black or similar
                - Size: 120-140px for impact
                - Weight: 800
                - Color: Solid vibrant colors (e.g Yellow, purple)
                - Position: 70% from top
                - Multi-color shadow outline
                - Add emojis to your text
                
                Secondary Text:
                - Size: 90-100px
                - Weight: 800
                - Color: Contrasting from main text
                - Spacing: 40px below main text
                - Matching shadow style
                
            3. TEXT TREATMENT
                Shadow Effects:
                - Contrasting color outline shadow
                - 4px offset in all directions
                - No black shadows (use bright colors)
                - Must use different shadow colors for each text element
                - Don't use gradients for the text colors only bright solid colors that standout
                - Add emojis to your text
                - Don't use white for the text color use some other popping brigth colors and a contrasting color for the shadow
                
            4. SPACING STRUCTURE
                - Top 60%: Clear for video preview
                - 70% mark: Text placement
                - Bottom 15%: Clear for UI elements
                
            ❌ FORBIDDEN:
            - Any overlays or gradients
            - Black shadows or dark effects
            - More than 2 text elements
            - Small or thin fonts
            - Centered text alignments
            - Image brightness adjustments
            - Using gradients in text colors.
            
            ✅ REQUIRED:
            - Full clear background image without overlays or gradients
            - Bold, colorful text
            - Contrasting shadow outlines
            - Text at 70% vertical position
            - Maximum readability
            - High-energy color combinations
        """,
        "usage_and_description": "Social media story thumbnail layout optimized for maximum visibility and engagement, featuring bold colored text with contrasting shadow outlines and clear background imagery."
    },
    "youtube_thumbnail_layout_1": {
        "layout_size": "1280px × 720px",
        "layout": """
            YouTube Thumbnail Layout

            1. CONTAINER STRUCTURE
                - Dimensions: 1280px × 720px
                - Background: Full video screenshot/image
                - No overlays or filters on background image
                - Image must be clearly visible

            2. TEXT POSITIONING
                Primary Layout Zones:
                - Right side text alignment (40-50% width)
                - Left side clear for background focus
                - Maintain 40px minimum edge spacing
                - Stack text blocks vertically with 8px gaps

            3. TEXT BLOCKS
                Structure:
                - Solid color background blocks behind all text
                - Padding: 10px 25px for each block
                - Box-shadow for subtle depth
                - Sharp, clean edges

                Color Rules:
                - Use vibrant, saturated colors (no black/white/grey)
                - Background colors: Deep, rich tones (#2C0066, #1A0044)
                - Text colors: Bright, popping shades (#00FFDD, #FFE249, #FF47B6)
                - Maintain high contrast between text and background

            4. TEXT HIERARCHY
                Main Text (Largest):
                - Font: Anton or similar ultra-bold font
                - Size: 130-140px
                - Weight: 800+
                - Use for numbers/money amounts

                Secondary Text:
                - Size: 90-100px
                - Weight: 800+
                - Use for main action/topic

                Supporting Text:
                - Size: 60-70px
                - Weight: 800+
                - Use for additional info

            5. SPACING & ALIGNMENT
                - Right-align all text blocks
                - Consistent vertical spacing (8px between blocks)
                - No random rotations or angles
                - Clean, structured layout

            ❌ FORBIDDEN:
            - Overlays on background image
            - Black or white colored blocks
            - Gradient effects
            - Centered text placement
            - Mixed text alignments
            - Rotated or skewed text
            - Grey scale colors
            - Text directly on image
            - More than 3 text blocks
            - Transparent backgrounds

            ✅ REQUIRED:
            - Solid color blocks behind all text
            - Vibrant color combinations
            - Right-side text alignment
            - Clean vertical stacking
            - Full visibility of background image
            - Maximum 3 text elements
            - Consistent text block styling
            - Sharp edges and corners
            - High contrast color pairs
        """,
        "usage_and_description": "Professional YouTube thumbnail layout optimized for maximum impact and readability, featuring bold text blocks with vibrant colors and clean right-side alignment. Perfect for gaming, challenge, or announcement videos where numbers or text need to stand out."
    }
}


def generate_thumbnail_design_prompt(video_details, image_url, layout_option):
    """Create the TikTok thumbnail design prompt"""
    prompt = f"""Generate a thumbnail design as a single HTML file with embedded CSS for:

    {video_details}

    You will be provided with an image example of how thumbnails can be designed as well, you can use the image as a reference to design the thumbnail.
    This examples have been designed by our team or generated by our AI during training previously and we consider them good examples for you to learn from without any copyright infringement.
    But stick to using the content details provided to you and not that on the design example, you're justs supposed to learn from the design.

    ESSENTIAL DESIGN PRINCIPLES:

    1. Layout Excellence
        - Design must be bold and attention-grabbing
        - Create strong visual emphasis on main text
        - Use dynamic text placement
        - Maintain Gen-Z aesthetic
        - Text must be instantly readable

    2. Visual Impact
        - Create viral-worthy first impression
        - Use vibrant colors
        - Text must pop from background
        - Strategic emoji placement
        - Maximum 3 text elements total

    3. Image Integration
        - Image must be high-energy and engaging
        - Image fills full container
        - Add subtle glow effects where needed
        - You have been provided with an image url use the image url: {image_url}
        - Try as much as possible to make the full image provided to you show in the design while keeping it at {layout_option["layout_size"]}
        - You can reduce from the height to keep the 100% proportion but make sure the whole width of the design shows and you don't cut out from that
        - If at all the width is too wide and out of proportion with the height to achieve a {layout_option["layout_size"]} design size then reduce from the left hand side

    4. Typography Excellence
        RULES:
        1. Font Requirements:
            - Use bold, impactful fonts (Inter Black, Poppins Black)
            - Main text: 72-84px size
            - Secondary text: 56-64px size
            - Highlight text: 48-56px size with background
            
        2. Text Positioning:
            - Main text at 65-70% from top
            - Clear spacing between text elements
            - Maximum 2-3 lines total
            

    5. Emoji Integration
        RULES:
        1. Placement Guidelines:
            - Inline emojis: Same size as text
            - Maximum 4 emojis total
            
        2. Size Requirements:
            - Inline emojis: Match text size
            - Background emojis: 1.5x text size
            
        3. Usage Rules:
            - Must be relevant to content
            - No repeated emojis
            - Strategic placement only
            - Must enhance, not distract
            
        4. Style Guidelines:
            - Add subtle shadow to emojis
            - Maintain proper spacing
            - Consider emoji meaning
            - Use trending emoji combinations

    6. Professional Refinements
        - Add glow effects for emphasis
        - Sharp, clean text edges
        - Professional drop shadows
        - Consistent styling throughout

    {layout_option["layout"]}

    7. Container Styling
        DIMENSIONS:
        - Main container: {layout_option["layout_size"]}
        - No padding (full bleed design)
        
        CONTENT DISTRIBUTION:
        - Top zone (0-60%): Keep clear for image focus
        - Text zone (60-85%): Main text content
        - Bottom zone (85-100%): Keep clear
        
        VALIDATION:
        □ Check text readability
        □ Verify emoji placement
        □ Confirm text contrast
        □ Test visual balance


    KEY STYLING RULES:
    - Typography: Bold and impactful
    - Contrast: High readability
    - Spacing: Clean and balanced
    - Emojis: Strategic placement
    - Text Shadow: Strong legibility
    - Colors: Vibrant and engaging

    OUTPUT: Generate only valid HTML/CSS code, no explanations.
    """
    return prompt


