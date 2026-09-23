from PIL import Image

def analyze():
    im = Image.open("D:/vphonewin/_work/latest_screen.png")
    w, h = im.size
    print(f"Image size: {w}x{h}")
    
    # Check 4 quadrants: (0, 0, w/2, h/2), (w/2, 0, w, h/2), etc.
    q1 = im.crop((0, 0, w//2, h//2))
    q2 = im.crop((w//2, 0, w, h//2))
    q3 = im.crop((0, h//2, w//2, h))
    q4 = im.crop((w//2, h//2, w, h))
    
    # Try horizontal stitching: Q1 left, Q2 right?
    # Or vertical: Q1 top, Q2 bottom?
    # Or 2x scale?
    
    # Let's create a stitched 512x2048 image (portrait phone format)
    portrait = Image.new("RGB", (w//2, h*2))
    portrait.paste(q1, (0, 0))
    portrait.paste(q2, (0, h//2))
    portrait.paste(q3, (0, h))
    portrait.paste(q4, (0, h + h//2))
    portrait.save("D:/vphonewin/_work/portrait_test.png")
    print("Saved portrait_test.png (512x2048)")
    
    # Let's create 1024x512
    wide = Image.new("RGB", (w*2, h//2))
    wide.paste(q1, (0, 0))
    wide.paste(q2, (w//2, 0))
    wide.paste(q3, (w, 0))
    wide.paste(q4, (w + w//2, 0))
    wide.save("D:/vphonewin/_work/wide_test.png")
    print("Saved wide_test.png (2048x512)")

if __name__ == '__main__':
    analyze()
