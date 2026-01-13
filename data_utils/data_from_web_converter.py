import requests
import re, json
import pandas as pd
from datetime import datetime


def find_flourish_id(url):
    print(f"🔎 Scanning: {url}")

    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        content = response.text

        # Pattern 1: Direct visualization link (common in iframes)
        # matches: flourish.studio/visualisation/1234567
        # matches: flo.uri.sh/visualisation/1234567
        viz_match = re.search(r"visualisation/(\d+)", content)

        # Pattern 2: Story link (stories are collections of visualizations)
        # matches: flourish.studio/story/1234567
        story_match = re.search(r"story/(\d+)", content)

        if viz_match:
            print(f"✅ Found Visualization ID: {viz_match.group(1)}")
            return viz_match.group(1)
        elif story_match:
            print(f"⚠️ Found Story ID: {story_match.group(1)} (Stories require different handling)")
            return story_match.group(1)
        else:
            # Fallback: Look for data-src attributes which often hold the ID
            data_src_match = re.search(r"data-src=[\"'](https://flo\.uri\.sh/visualisation/(\d+)/embed)[\"']", content)
            if data_src_match:
                print(f"✅ Found Data-Src ID: {data_src_match.group(2)}")
                return data_src_match.group(2)

            print("❌ No Flourish ID found in the page source.")
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def dump_raw_flourish_text(visualisation_id, output_file_path):
    url = f"https://flo.uri.sh/visualisation/{visualisation_id}/embed"
    print(f"Fetching raw HTML from: {url}")

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    html_content = response.text

    # Find where the variable assignment starts
    # We look for "_Flourish_data ="
    match = re.search(r"_Flourish_data\s*=\s*", html_content)

    if not match:
        print("Could not find '_Flourish_data' in the page source.")
        return

    print("Found data start point. Extracting raw text chunk...")

    # Start capturing right after "_Flourish_data ="
    start_index = match.end()

    # We will grab a large chunk (e.g., 500,000 characters) to ensure we get everything.
    # We assume the data ends with a semicolon usually, but we'll grab extra to be safe.
    raw_chunk = html_content[start_index: start_index + 500000]

    # OPTIONAL: precise slicing
    # Try to cut it off at the next script tag if possible to keep it cleaner
    if "</script>" in raw_chunk:
        raw_chunk = raw_chunk.split("</script>")[0]

    # Save to a text file
    filename = output_file_path
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(raw_chunk)

    print(f"✅ Raw data dumped to '{output_file_path}'")
    print(" You can now open this file in a text editor to view the structure.")


def decode_and_export_flourish(input_file_path,output_file_path):
    print(f"📂 Reading raw file: {input_file_path}")

    with open(input_file_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # --- Step 1: Clean JavaScript Syntax ---
    # Replace "new Date(123456789)" with just the number "123456789"
    # This makes it valid for the JSON parser
    clean_text = re.sub(r'new Date\((-?\d+)\)', r'\1', raw_text)

    # --- Step 2: Robust Parsing ---
    # Find the very first '{' which starts the data object
    start_index = clean_text.find('{')

    if start_index == -1:
        print("❌ Could not find start of JSON object '{'")
        return

    try:
        # raw_decode parses one valid JSON object and ignores the rest of the string
        decoder = json.JSONDecoder()
        data, _ = decoder.raw_decode(clean_text[start_index:])
        print("✅ JSON parsed successfully!")

    except json.JSONDecodeError as e:
        print(f"❌ JSON Decode Error: {e}")
        return

    # --- Step 3: Extract Data ---
    if "points" not in data:
        print("❌ Could not find 'points' list in the data.")
        return

    points = data["points"]
    print(f"📊 Processing {len(points)} data points...")

    extracted_rows = []

    for p in points:
        # Basic Info
        name = p.get("label", "N/A")
        lat = p.get("lat")
        lon = p.get("lon")

        # Metadata mapping based on your file structure:
        # 0: Funding, 1: Color, 2: Agency Short, 3: Agency Full,
        # 4: Institution, 5: Date, 6: Focus Area, 7: Website
        meta = p.get("metadata", [])

        # Helper to get metadata safely
        def get_meta(idx):
            return meta[idx] if meta and len(meta) > idx and meta[idx] is not None else ""

        funding = get_meta(0)
        agency_short = get_meta(2)  # Prefer metadata agency over point color
        agency_full = get_meta(3)
        institution = get_meta(4)
        focus_area = get_meta(6)
        website = get_meta(7)

        # Date Parsing (Handle timestamps from the Regex fix)
        raw_date = get_meta(5)
        founding_date = ""
        if isinstance(raw_date, (int, float)):
            try:
                # Timestamps usually ms
                dt = datetime.fromtimestamp(raw_date / 1000)
                founding_date = dt.strftime('%Y-%m-%d')
            except:
                founding_date = str(raw_date)

        extracted_rows.append({
            "Name": name,
            "Institution": institution,
            "Agency": agency_short,
            "Agency Full": agency_full,
            "Focus Area": focus_area,
            "Funding": funding,
            "Founding Date": founding_date,
            "Latitude": lat,
            "Longitude": lon,
            "Website": website
        })

    # --- Step 4: Save to CSV ---
    df = pd.DataFrame(extracted_rows)

    # Reorder columns nicely
    cols = ["Name", "Institution", "Agency", "Focus Area", "Founding Date",
            "Funding", "Latitude", "Longitude", "Website", "Agency Full"]
    # Filter to only columns that exist
    df = df[[c for c in cols if c in df.columns]]

    df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

    print(f"🎉 Success! Saved to: {output_file_path}")
    print(df.head())



