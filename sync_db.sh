#!/bin/bash
# Move downloaded data.db into moneymanager project

DOWNLOADS=~/Downloads/data.db
TARGET=~/moneymanager/data.db

if [ -f "$DOWNLOADS" ]; then
    mv "$DOWNLOADS" "$TARGET"
    echo "✅ Synced database to moneymanager folder."
else
    echo "❌ No data.db found in Downloads."
fi

