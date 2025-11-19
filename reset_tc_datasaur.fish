#!/usr/bin/env fish

set EXPORT_FOLDER ~/HoardingDisorderData/data/mathews/documents/datasaur_exports/
set TC_FOLDER $EXPORT_FOLDER/truncated_clauses/
set BACKUP_ZIP $EXPORT_FOLDER/exported_truncated_clauses_label_data_from_datasaur.zip

if test -d $TC_FOLDER
    rm -r $TC_FOLDER
    echo "Removed existing truncated clauses folder."
end

if test -f $BACKUP_ZIP
    unzip $BACKUP_ZIP -d $EXPORT_FOLDER
    echo "Unzipped backup truncated clauses data."
end