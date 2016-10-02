package com.mooncheesez.testapplication;

import android.content.Intent;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.MotionEvent;
import android.view.View;
import android.view.Menu;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity {
    // Intent key values
    public final static String EXTRA_NAME = "com.mooncheesez.testapplication.NAME";
    public final static String EXTRA_VALUE = "com.mooncheesez.testapplication.VALUE";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Set title
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        getSupportActionBar().setTitle("Database");

        // Make layout focusable to remove focus from fields
        findViewById(R.id.content_main).setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                InputMethodManager imm = (InputMethodManager) getSystemService(
                        INPUT_METHOD_SERVICE);
                imm.hideSoftInputFromWindow(getCurrentFocus().getWindowToken(), 0);
                return false;
            }
        });

        // Set floating action button to delete values table from database.
        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Are you sure you want to clear the database?",
                        Snackbar.LENGTH_LONG).setAction("Clear", new View.OnClickListener() {
                            @Override
                            public void onClick(View view) {
                                TestDbAdapter dbAdapter = new TestDbAdapter(getApplicationContext());
                                dbAdapter.open();
                                dbAdapter.deleteAll();
                                dbAdapter.close();
                            }
                        }).show();
            }
        });

        // Send to another activity via submit button
        Button button = (Button) findViewById(R.id.submit);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                EditText nameField = (EditText) findViewById(R.id.nameTextField);
                EditText valueField = (EditText) findViewById(R.id.valueTextField);

                Intent intent = new Intent(getApplicationContext(), DatabaseViewActivity.class);
                intent.putExtra(EXTRA_NAME, nameField.getText().toString());
                intent.putExtra(EXTRA_VALUE, valueField.getText().toString());
                startActivity(intent);
            }
        });

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        // getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

//    @Override
//    public boolean onOptionsItemSelected(MenuItem item) {
//        // Handle action bar item clicks here. The action bar will
//        // automatically handle clicks on the Home/Up button, so long
//        // as you specify a parent activity in AndroidManifest.xml.
//        int id = item.getItemId();
//
//        //noinspection SimplifiableIfStatement
//        if (id == R.id.action_settings) {
//            return true;
//        }
//
//        return super.onOptionsItemSelected(item);
//    }
}
