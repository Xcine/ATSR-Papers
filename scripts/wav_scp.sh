path="data/malfong/train/"
utils="utils"
prepa="prepa"

# Create the wav.scp file
echo "#########"
echo "Creation of the wav.scp file mapping recording ids with files"
python3 $prepa/create_wav_scp.py
echo "#########"

# Fix the data directory
echo "#########"
echo "Fixing the repeated data and the ordering in wav.scp file"
$utils/fix_data_dir.sh $path
echo "#########"

# Validate the data directory
echo "#########"
echo "Validating data directory without feats.scp"
$utils/validate_data_dir.sh --no-feats $path
echo "#########"
