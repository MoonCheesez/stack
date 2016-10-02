package com.mooncheesez.testapplication;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.util.Log;

import java.util.ArrayList;

class TestDbAdapter {
    // Define constants
    // Constants for database
    private static final String DATABASE_NAME = "test.db";
    private static final int DATABASE_VERSION = 1;
    // Constants for values table
    private static final String VALUES_TABLE = "values_table";
    private static final String COLUMN_ID = "id";
    private static final String COLUMN_NAME = "name";
    private static final String COLUMN_VALUE = "val";
    // Columns list
    private String[] COLUMNS = {COLUMN_ID, COLUMN_NAME, COLUMN_VALUE};

    // String to create database
    private static final String CREATE_TABLE_VALUES = "CREATE TABLE " + VALUES_TABLE + "("
            + COLUMN_ID + " INTEGER PRIMARY KEY AUTOINCREMENT, "
            + COLUMN_NAME + " TEXT NOT NULL, "
            + COLUMN_VALUE + " TEXT NOT NULL "
            + ");";

    // Class variables
    private SQLiteDatabase SQLdb;
    private ValuesDbHelper valuesDbHelper;
    private Context context;

    TestDbAdapter(Context ctx) {
        context = ctx;
    }

    // Open Database
    public TestDbAdapter open() throws android.database.SQLException {
        valuesDbHelper = new ValuesDbHelper(context);
        SQLdb = valuesDbHelper.getWritableDatabase();
        return this;
    }
    // Close Database
    void close() {
        valuesDbHelper.close();
    }

    // Add new entry
    void insertValue(Value value) {
        ContentValues values = new ContentValues();

        values.put(TestDbAdapter.COLUMN_NAME, value.name);
        values.put(TestDbAdapter.COLUMN_VALUE, value.value);

        SQLdb.insert(TestDbAdapter.VALUES_TABLE, null, values);
    }
    // Get entries
    ArrayList<Value> readValues() {
        ArrayList<Value> values = new ArrayList<>();

        Cursor cursor = SQLdb.query(VALUES_TABLE, COLUMNS, null, null, null, null, null);

        for (cursor.moveToLast(); !cursor.isBeforeFirst(); cursor.moveToPrevious()) {
            values.add(new Value(cursor.getString(1), cursor.getString(2)));
        }
        cursor.close();

        return values;
    }
    // Delete all entries
    void deleteAll() {
        SQLdb.execSQL("DROP TABLE IF EXISTS " + VALUES_TABLE);
        valuesDbHelper.onCreate(SQLdb);
    }

    // Database helper
    private static class ValuesDbHelper extends SQLiteOpenHelper {
        ValuesDbHelper(Context ctx) {
            super(ctx, DATABASE_NAME, null, DATABASE_VERSION);
        }

        @Override
        public void onCreate(SQLiteDatabase db) {
            db.execSQL(CREATE_TABLE_VALUES);
        }

        @Override
        public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
            Log.w(ValuesDbHelper.class.getName(),
                    "Updating database from version " + oldVersion + " to " + newVersion + "." +
                            " This will destroy all data.");
            db.execSQL("DROP TABLE IF EXISTS " + VALUES_TABLE);
            onCreate(db);
        }
    }
}
