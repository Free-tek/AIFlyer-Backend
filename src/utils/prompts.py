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

layout_options = {
    "full_background_image": 
        {"layout": """
            Full-Image Background Layout
    
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
         "usage_and_description": "This layout is a pattern background layout that uses the brands color for the pattern and then the text ontop of it."},

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
    }
}

def generate_initial_design_prompt(business_details, image_url, other_images, layout_option):
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
        - Use modern border-radius (20px for containers, 30px for call to actions)
        - Maintain consistent spacing rhythm

    7. Content Guidelines ⚠️ MANDATORY TEXT CONTENT
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
            - Maintain minimum 24px spacing between elements
            - Ensure no overlap after adjustments
            - Validate new positions don't create new conflicts

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