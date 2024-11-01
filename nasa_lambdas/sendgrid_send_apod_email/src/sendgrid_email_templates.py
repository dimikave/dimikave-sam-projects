def generate_email_template(greeting, title, url, explanation, mysterious_content, space_fact):
    """
    Generate an HTML email template for NASA's Astronomy Picture of the Day.

    Args:
        greeting (str): Personalized greeting for the email.
        title (str): Title of the APOD.
        url (str): URL of the APOD image.
        explanation (str): Explanation of the APOD.
        mysterious_content (str): Generated mysterious content about space.
        space_fact (str): Generated interesting space fact.

    Returns:
        str: HTML content for the email.
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NASA's Astronomy Picture of the Day</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #0a0a2a; color: #ffffff;">
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; margin: 0 auto; background-color: #1a1a4a;">
        <tr>
            <td style="padding: 20px; text-align: center; background-color: #1a237e;">
                <h1 style="margin: 0; font-size: 24px; color: #ffffff;">NASA's Astronomy Picture of the Day</h1>
            </td>
        </tr>
        <tr>
            <td style="padding: 20px;">
                <h2 style="color: #ffffff;">{greeting}</h2>
                <h3 style="color: #00ffff;">{title}</h3>
                <img src="{url}" alt="{title}" style="max-width: 100%; height: auto; border-radius: 8px; margin-bottom: 15px;">
                <p style="color: #af2f6f;">{mysterious_content}</p>
                <div style="background-color: #2a2a6a; border-left: 4px solid #00ffff; padding: 15px; margin: 15px 0;">
                <strong style="color: #00ffff;">Picture of the day description:</strong>
                 <span style="color: #ffffff;">{explanation}</span>
                </div>
                <div style="background-color: #2a2a6a; border-left: 4px solid #00ffff; padding: 15px; margin: 15px 0;">
                    <strong style="color: #00ffff;">Did you know?</strong> 
                    <span style="color: #ffffff;">{space_fact}</span>
                </div>
                <p style="color: #ffffff;">Embark on this cosmic journey and find the image history on <a href="https://apod.nasa.gov/apod/archivepix.html" style="color: #00ffff; text-decoration: none;">NASA APOD archive</a>.</p>
            </td>
        </tr>
        <tr>
            <td style="padding: 20px; text-align: center; background-color: #1a237e; color: #ffffff;">
                <p style="margin: 0; font-size: 14px;">&copy; Brought to you by your space invader Dimitris Kavelidis</p>
            </td>
        </tr>
    </table>
</body>
</html>
"""
