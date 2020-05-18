package com.example.vexillum;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.TextView;

public class NotificationActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_notification);

        Intent intent = getIntent();
        String body = intent.getStringExtra("Body");

        TextView infoText = this.findViewById(R.id.infoTextView);
        infoText.setText(body);
    }
}
