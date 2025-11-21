#!/usr/bin/env fish

set EXPORT_FOLDER (realpath ~/HoardingDisorderScripts/data/mathews/documents/datasaur_exports/)
set TC_FOLDER $EXPORT_FOLDER/truncated_clauses/
set BACKUP_ZIP $EXPORT_FOLDER/exported_truncated_clauses_label_data_from_datasaur.zip

if test -z "$EXPORT_FOLDER"
    echo "❌ Could not find export folder at $EXPORT_FOLDER."
    exit 1
end

if test -d $TC_FOLDER
    rm -rv $TC_FOLDER
    echo "✅ Removed existing truncated clauses folder at $TC_FOLDER."
else
    exit 1
end

if test -f $BACKUP_ZIP
    unzip $BACKUP_ZIP -d $EXPORT_FOLDER
    echo "✅ Unzipped backup truncated clauses data at $BACKUP_ZIP."
else
    exit 1
end

echo "✅ Done."