import streamlit as st
import uuid
from datetime import datetime
from geopy.geocoders import Nominatim
import time

# Streamlit App Configuration
st.set_page_config(page_title="Water Issues Reporter - Mbeya", layout="wide")

# Language Options
LANGUAGES = {
    "English": {
        "title": "💧 Water Issues Reporter",
        "report_type_label": "What would you like to report?",
        "report_types": {
            "leakage": "Water Leakage",
            "quality": "Water Quality Issue"
        },
        "report_tab": "Report Issue",
        "view_tab": "View Reports",
        "new_report_header": "Report New Issue",
        "location_step": "Step 1: Confirm Location",
        "detected_location": "📍 Detected Location:",
        "latitude": "Latitude:",
        "longitude": "Longitude:",
        "accuracy": "Accuracy:",
        "confirm_location": "✅ Confirm Location",
        "detect_again": "🔄 Detect Again",
        "details_step": "Step 2: Issue Details",
        "take_photo": "1. Take Photo with Camera",
        "camera_instruction": {
            "leakage": "Point your camera at the leakage and take a photo",
            "quality": "Point your camera at the water source and take a photo"
        },
        "upload_photo": "2. Or Upload Existing Photo",
        "description_header": "3. Issue Description",
        "description_placeholder": {
            "leakage": "Describe the leakage (required)...\n\nExample: 'Broken pipe causing water flow at street corner'",
            "quality": "Describe the water quality issue (required)...\n\nExample: 'Brown water coming from taps with strange odor'"
        },
        "severity_label": "Severity Level",
        "submit_button": "📤 Submit Report",
        "water_quality_label": "Water Quality",
        "quality_options": ["Clear", "Cloudy", "Brown/Dirty", "Contaminated", "Other"],
        "no_description_error": "Please provide a description",
        "success_message": "Report submitted successfully!",
        "your_reports": "Your Reports",
        "no_reports": "No reports found. Submit your first report using the 'Report Issue' tab.",
        "report_expander": "{} Report {} - {} ({})",
        "status_label": "Status:",
        "severity_label_view": "Severity:",
        "date_label": "Date:",
        "coordinates_label": "Coordinates:",
        "description_label": "Description:",
        "quality_label": "Water Quality:",
        "type_label": "Type:",
        "logout_button": "Logout",
        "logged_in_as": "Logged in as {}"
    },
    "Swahili": {
        "title": "💧 Ripoti ya Matatizo ya Maji",
        "report_type_label": "Unataka kuripoti nini?",
        "report_types": {
            "leakage": "Uvujaji wa Maji",
            "quality": "Ubora wa Maji"
        },
        "report_tab": "Ripoti Tatizo",
        "view_tab": "Tazama Ripoti",
        "new_report_header": "Ripoti Tatizo Jipya",
        "location_step": "Hatua ya 1: Thibitisha Eneo",
        "detected_location": "📍 Eneo Lililogunduliwa:",
        "latitude": "Latitudo:",
        "longitude": "Longitudo:",
        "accuracy": "Usahihi:",
        "confirm_location": "✅ Thibitisha Eneo",
        "detect_again": "🔄 Gundua Tena",
        "details_step": "Hatua ya 2: Maelezo ya Tatizo",
        "take_photo": "1. Piga Picha kwa Kamera",
        "camera_instruction": {
            "leakage": "Elekeza kamera kwenye uvujaji na upige picha",
            "quality": "Elekeza kamera kwenye chanzo cha maji na upige picha"
        },
        "upload_photo": "2. Au Pakia Picha Iliyopo",
        "description_header": "3. Maelezo ya Tatizo",
        "description_placeholder": {
            "leakage": "Eleza uvujaji (inahitajika)...\n\nMfano: 'Bomba lililovunjika linasababisha maji kutiririka kwenye kona ya barabara'",
            "quality": "Eleza tatizo la ubora wa maji (inahitajika)...\n\nMfano: 'Maji yenye rangi ya kahawia yanayotoka kwenye bomba na harufu mbaya'"
        },
        "severity_label": "Kiwango cha Tatizo",
        "submit_button": "📤 Wasilisha Ripoti",
        "water_quality_label": "Ubora wa Maji",
        "quality_options": ["Safi", "Kuna mawingu", "Kahawia/Chafu", "Iliyo na uchafu", "Nyingine"],
        "no_description_error": "Tafadhali toa maelezo",
        "success_message": "Ripoti imewasilishwa kikamilifu!",
        "your_reports": "Ripoti Zako",
        "no_reports": "Hakuna ripoti zilizopatikana. Wasilisha ripoti yako ya kwanza kwa kutumia kichupo 'Ripoti Tatizo'.",
        "report_expander": "{} Ripoti {} - {} ({})",
        "status_label": "Hali:",
        "severity_label_view": "Kiwango:",
        "date_label": "Tarehe:",
        "coordinates_label": "Kuratibu:",
        "description_label": "Maelezo:",
        "quality_label": "Ubora wa Maji:",
        "type_label": "Aina:",
        "logout_button": "Ondoka",
        "logged_in_as": "Umeingia kama {}"
    }
}

# Initialize Session State
if 'user' not in st.session_state:
    st.session_state.user = {
        "email": "guest@example.com",
        "uid": "guest123"
    }
if 'reports' not in st.session_state:
    st.session_state.reports = []
if 'location' not in st.session_state:
    st.session_state.location = None
if 'location_confirmed' not in st.session_state:
    st.session_state.location_confirmed = False
if 'language' not in st.session_state:
    st.session_state.language = "English"
if 'report_type' not in st.session_state:
    st.session_state.report_type = "leakage"

# Helper Functions
def get_location_name(lat, lon):
    try:
        geolocator = Nominatim(user_agent="water_issues_reporter_mbeya")
        location = geolocator.reverse(f"{lat}, {lon}", timeout=10)
        return location.address if location else "Mbeya, Tanzania"
    except:
        return "Mbeya, Tanzania"

def get_current_location():
    """Default location set to Mbeya, Tanzania"""
    return {
        "latitude": -8.9094,
        "longitude": 33.4608,
        "accuracy": 100,
        "address": "Mbeya, Tanzania",
        "source": "default"
    }

def show_auth_status():
    lang = LANGUAGES[st.session_state.language]
    
    if st.session_state.user and isinstance(st.session_state.user, dict) and 'email' in st.session_state.user:
        st.sidebar.success(lang["logged_in_as"].format(st.session_state.user['email']))
    else:
        st.sidebar.warning("Not logged in" if st.session_state.language == "English" else "Haijaingia")
        st.session_state.user = {
            "email": "guest@example.com",
            "uid": "guest123"
        }
    
    if st.sidebar.button(lang["logout_button"]):
        st.session_state.user = None
        st.rerun()

# Main App Function
def main():
    # Language Selector
    lang_key = st.sidebar.selectbox(
        "Language / Lugha",
        options=list(LANGUAGES.keys()),
        index=0 if st.session_state.get('language', "English") == "English" else 1
    )
    st.session_state.language = lang_key
    lang = LANGUAGES[st.session_state.language]
    
    st.title(lang["title"])
    show_auth_status()
    
    tab1, tab2 = st.tabs([lang["report_tab"], lang["view_tab"]])
    
    with tab1:
        st.header(lang["new_report_header"])
        
        # Report Type Selection
        report_type = st.radio(
            lang["report_type_label"],
            options=list(lang["report_types"].values()),
            index=0 if st.session_state.report_type == "leakage" else 1
        )
        st.session_state.report_type = "leakage" if report_type == lang["report_types"]["leakage"] else "quality"
        
        if not st.session_state.location_confirmed:
            st.subheader(lang["location_step"])
            if not st.session_state.location:
                st.session_state.location = get_current_location()
            
            location_source = " (using your device GPS)" if st.session_state.location.get('source') == "device" else " (default Mbeya location)"
            
            st.write(f"{lang['detected_location']} **{get_location_name(st.session_state.location['latitude'], st.session_state.location['longitude'])}**{location_source}")
            st.write(f"{lang['latitude']} {st.session_state.location['latitude']:.6f}")
            st.write(f"{lang['longitude']} {st.session_state.location['longitude']:.6f}")
            if st.session_state.location.get('accuracy'):
                st.write(f"{lang['accuracy']} ±{st.session_state.location['accuracy']} meters")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(lang["confirm_location"], use_container_width=True):
                    st.session_state.location_confirmed = True
                    st.rerun()
            with col2:
                if st.button(lang["detect_again"], use_container_width=True):
                    st.session_state.location = get_current_location()
                    st.rerun()
            return
        
        with st.form("report_form"):
            st.subheader(lang["details_step"])
            
            st.write(f"**{lang['detected_location'].replace(':', '')}**", get_location_name(
                st.session_state.location['latitude'],
                st.session_state.location['longitude']
            ))
            st.write(f"{lang['latitude']} {st.session_state.location['latitude']:.6f}")
            st.write(f"{lang['longitude']} {st.session_state.location['longitude']:.6f}")
            
            # Camera Input
            st.subheader(lang["take_photo"])
            st.info(lang["camera_instruction"][st.session_state.report_type])
            img_file_buffer = st.camera_input("Take a picture", label_visibility="collapsed")
            
            # File Uploader
            st.subheader(lang["upload_photo"])
            uploaded_file = st.file_uploader("Select image from your device", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
            
            # Description
            st.subheader(lang["description_header"])
            description = st.text_area(
                lang["description_header"].replace("3. ", ""),
                placeholder=lang["description_placeholder"][st.session_state.report_type],
                height=150
            )
            
            severity = st.select_slider(
                lang["severity_label"],
                options=["Low", "Medium", "High", "Critical"],
                value="Medium"
            )
            
            # Water Quality Selection
            water_quality = st.selectbox(
                lang["water_quality_label"],
                options=lang["quality_options"]
            )
            
            submitted = st.form_submit_button(lang["submit_button"], type="primary")
            
            if submitted:
                if not description:
                    st.error(lang["no_description_error"])
                    return
                
                try:
                    report_id = str(uuid.uuid4())
                    report_data = {
                        "id": report_id,
                        "type": st.session_state.report_type,
                        "type_name": lang["report_types"][st.session_state.report_type],
                        "user_email": st.session_state.user['email'],
                        "user_id": st.session_state.user['uid'],
                        "location": {
                            "latitude": st.session_state.location['latitude'],
                            "longitude": st.session_state.location['longitude']
                        },
                        "description": description,
                        "severity": severity,
                        "water_quality": water_quality,
                        "status": "Pending",
                        "timestamp": datetime.now(),
                        "has_image": img_file_buffer is not None or uploaded_file is not None,
                        "region": "Mbeya"
                    }
                    
                    st.session_state.reports.append(report_data)
                    st.success(lang["success_message"])
                    
                    st.session_state.location = None
                    st.session_state.location_confirmed = False
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with tab2:
        st.header(lang["your_reports"])
        
        if not st.session_state.reports:
            st.info(lang["no_reports"])
            return
        
        for report in sorted(st.session_state.reports, key=lambda x: x['timestamp'], reverse=True):
            with st.expander(lang["report_expander"].format(
                report['type_name'],
                report['id'][:8], 
                report['status'], 
                report['severity']
            ), expanded=False):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    if report.get('has_image'):
                        st.image("https://via.placeholder.com/250x150?text=Issue+Photo", width=250)
                    else:
                        st.warning("No image attached" if st.session_state.language == "English" else "Hakuna picha iliyobatanishwa")
                    
                    st.write(f"**{lang['type_label']}** {report['type_name']}")
                    st.write(f"**{lang['status_label']}** {report['status']}")
                    st.write(f"**{lang['severity_label_view']}** {report['severity']}")
                    st.write(f"**{lang['date_label']}** {report['timestamp'].strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**{lang['quality_label']}** {report['water_quality']}")
                
                with col2:
                    location_name = get_location_name(
                        report['location']['latitude'],
                        report['location']['longitude']
                    )
                    st.write(f"**{lang['detected_location'].replace(':', '')}** {location_name}")
                    st.write(f"**{lang['coordinates_label']}** {report['location']['latitude']:.6f}, {report['location']['longitude']:.6f}")
                    st.write(f"**{lang['description_label']}**")
                    st.write(report['description'])

if __name__ == "__main__":
    main()