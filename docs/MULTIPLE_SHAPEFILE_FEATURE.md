# 📂 Multiple Shapefile Selection Feature

## Overview

The mLS Calculator now supports ZIP files containing **multiple shapefiles**! When you upload a ZIP with more than one shapefile, you'll be presented with a selection interface to choose which one to analyze.

## ✨ New Feature

### What's New

- **Automatic Detection**: System automatically scans the ZIP for all `.shp` files
- **Selection Interface**: Clean, intuitive UI to pick the shapefile you want
- **Recursive Search**: Finds shapefiles even in subdirectories within the ZIP
- **Parameter Persistence**: Your optional parameters (cutoff, beta, errors) are preserved
- **Visual Feedback**: Selected shapefile is highlighted

### How It Works

1. **Upload ZIP**: Upload a ZIP file as usual
2. **Detection**: System finds all shapefiles inside
3. **Selection Page** (if multiple found):
   - Shows list of all shapefiles
   - Displays filename and path
   - Radio button selection
   - Same parameter input fields
4. **Processing**: Selected shapefile is analyzed
5. **Results**: Standard results page with shapefile name displayed

## 🎯 Use Cases

### Scenario 1: Multiple Study Areas
Your ZIP contains:
- `landslides_area1.shp`
- `landslides_area2.shp`
- `landslides_area3.shp`

→ Select one area to analyze at a time

### Scenario 2: Different Time Periods
Your ZIP contains:
- `landslides_2020.shp`
- `landslides_2021.shp`
- `landslides_2022.shp`

→ Compare mLS values across years

### Scenario 3: Nested Structure
Your ZIP structure:
```
landslide_data/
  ├── region1/
  │   └── inventory.shp
  └── region2/
      └── inventory.shp
```

→ System finds both, shows relative paths

## 📋 User Interface

### Selection Page Elements

1. **Warning Box** (Yellow):
   - Alerts user that multiple shapefiles were found
   - Explains what to do

2. **Shapefile List**:
   - Each option shows:
     - ✅ Radio button for selection
     - 📄 Filename (bold, large text)
     - 📁 Full path (smaller, monospace)
   - Hover effect (changes color, slides right)
   - Selected option highlighted with blue gradient

3. **Parameters Section**:
   - Same as main upload page
   - Pre-filled if values were entered on upload page
   - Can be changed before processing

4. **Action Buttons**:
   - **Calculate mLS** (primary) - Process selected shapefile
   - **Upload Different File** (secondary) - Start over

### Visual Design

- **Responsive**: Works on all screen sizes
- **Accessible**: Clear labels, keyboard navigation
- **Intuitive**: First shapefile pre-selected
- **Consistent**: Matches overall app design

## 🔧 Technical Details

### Backend Changes

#### `extract_shapefile()` Function
**Before:**
```python
def extract_shapefile(zip_path, extract_dir):
    # Returns single shapefile path
    return os.path.join(extract_dir, shp_files[0])
```

**After:**
```python
def extract_shapefile(zip_path, extract_dir):
    # Returns list of all shapefile paths
    return shp_files  # List of relative paths
```

#### New Route: `/process_selected`
- Handles shapefile selection
- Retrieves temp_dir and selected_shp from form
- Processes areas and calculates mLS
- Returns results page

#### Updated Route: `/upload`
- Detects multiple shapefiles
- Shows selection page if len(shp_files) > 1
- Otherwise processes directly (original behavior)

### Frontend Changes

#### New Template: `select_shapefile.html`
- Extends `base.html`
- Radio button list for shapefiles
- Parameter input fields
- JavaScript for visual feedback

#### Updated Template: `results.html`
- Shows shapefile name at top of results
- Helps identify which file was analyzed

## 📊 Testing

### Test Data Generated

Two ZIP files are now available:

1. **`test_landslides.zip`** (1 shapefile)
   - 500 synthetic landslides
   - Tests standard workflow

2. **`multiple_landslides.zip`** (2 shapefiles)
   - `landslides_inventory1.shp` - 400 features
   - `landslides_inventory2.shp` - 500 features
   - Tests selection feature

### Test Cases

✅ **Single Shapefile**: Goes directly to processing (no change)
✅ **Multiple Shapefiles**: Shows selection page
✅ **Parameter Persistence**: Values carried over from upload page
✅ **Path Display**: Shows relative paths correctly
✅ **Nested Directories**: Finds shapefiles in subdirectories
✅ **Results Display**: Shows selected shapefile name

## 🚀 Usage Examples

### Example 1: Basic Selection

```
1. Upload multiple_landslides.zip
2. See selection page with 2 options
3. Choose "landslides_inventory2.shp"
4. Click "Calculate mLS"
5. View results for inventory 2
```

### Example 2: With Parameters

```
1. Upload multiple_landslides.zip
2. On upload page, enter:
   - Cutoff: 150
   - Beta: -2.3
3. See selection page (parameters preserved)
4. Choose shapefile
5. Modify parameters if needed
6. Calculate
```

### Example 3: Compare Multiple Inventories

```
For each shapefile in the ZIP:
1. Upload ZIP
2. Select shapefile A
3. Note mLS value
4. Go back, upload same ZIP
5. Select shapefile B
6. Note mLS value
7. Compare results
```

## 🎨 Visual Workflow

```
Upload ZIP
    ↓
Extract & Scan
    ↓
┌───────────────────────┐
│ Multiple .shp files?  │
└───────────────────────┘
    ↙           ↘
  YES           NO
    ↓            ↓
Selection    Direct
  Page     Processing
    ↓            ↓
  Select    ← ← ←┘
Shapefile
    ↓
 Process
    ↓
 Results
```

## 💡 Benefits

### For Users
- ✅ **No need to manually separate files**
- ✅ **Upload once, analyze multiple**
- ✅ **Clear visualization of options**
- ✅ **Easy to switch between inventories**
- ✅ **Parameter reuse across selections**

### For Workflows
- ✅ **Batch inventory management**
- ✅ **Temporal comparisons**
- ✅ **Regional analysis**
- ✅ **Quality control** (test vs production data)

## 🔄 Backward Compatibility

✅ **Fully backward compatible!**

- Single shapefile ZIPs work exactly as before
- No changes to existing workflows
- Selection page only appears when needed

## 📝 Notes

### Temporary Storage
- System uses temporary directories for extraction
- Cleaned up after processing
- Multiple users don't interfere with each other

### File Validation
- Still validates shapefile components (.shx, .dbf, .prj)
- Validation happens after selection

### Performance
- Scanning for shapefiles is very fast
- No significant performance impact

## 🎉 Summary

The **multiple shapefile selection feature** makes the mLS Calculator more flexible and user-friendly, especially for:
- Researchers with multiple study areas
- Temporal analysis projects
- Batch processing workflows
- Organized data archives

**Test it now** with `multiple_landslides.zip`!

---

**Server running at:** http://localhost:5001

**Try uploading:**
- `test_landslides.zip` → Direct processing (1 shapefile)
- `multiple_landslides.zip` → Selection page (2 shapefiles)
