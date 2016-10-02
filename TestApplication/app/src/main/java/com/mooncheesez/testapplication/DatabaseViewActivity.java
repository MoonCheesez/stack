package com.mooncheesez.testapplication;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.widget.NestedScrollView;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.TypedValue;
import android.widget.GridLayout;
import android.widget.TextView;

import java.util.ArrayList;

/**
 * This activity displays the values stored in the database.
 * It does so by:
 *  Get intent from previous activity
 *  Open database
 *  Add values from intent of previous activity into database
 *  Read all values from database
 *  Close database
 *  Display information read
 */
public class DatabaseViewActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_database_view);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        // Get intent
        Intent intent = getIntent();

        // Open database
        TestDbAdapter dbAdapter = new TestDbAdapter(getBaseContext());
        dbAdapter.open();
        // Insert new values from intent into database
        dbAdapter.insertValue(new Value(intent.getStringExtra(MainActivity.EXTRA_NAME),
                                        intent.getStringExtra(MainActivity.EXTRA_VALUE)));
        // Read values from database
        ArrayList<Value> values = dbAdapter.readValues();
        // Close database
        dbAdapter.close();

        // Get GridLayout view
        GridLayout value_layout = (GridLayout) findViewById(R.id.database_content);
        value_layout.setRowCount(values.size());

        // Display each value read from database into grid layout
        for (int i=0; i<values.size(); i++) {
            // Get value from values
            Value val = values.get(i);

            // Name TextView
            TextView nameView = new TextView(this);
            nameView.setText(val.name);
            nameView.setTextSize(TypedValue.COMPLEX_UNIT_SP, 19);
            // Value TextView
            TextView valueView = new TextView(this);
            valueView.setText(val.value);
            valueView.setTextSize(TypedValue.COMPLEX_UNIT_SP, 19);

            // Set GridLayout parameters for nameView
            GridLayout.LayoutParams namelayoutParams = new GridLayout.LayoutParams();
            namelayoutParams.rowSpec = GridLayout.spec(i, 1);
            namelayoutParams.columnSpec = GridLayout.spec(0, 1, 1f);
            // Add nameView to GridLayout
            value_layout.addView(nameView, namelayoutParams);

            // Set GridLayout parameters for valueView
            GridLayout.LayoutParams valuelayoutParams = new GridLayout.LayoutParams();
            valuelayoutParams.rowSpec = GridLayout.spec(i, 1);
            valuelayoutParams.columnSpec = GridLayout.spec(1, 1, 1f);
            // Add valueView to GridLayout
            value_layout.addView(valueView, valuelayoutParams);
        }
    }
}
