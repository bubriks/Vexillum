package com.example.vexillum;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import com.google.firebase.auth.FirebaseAuth;

public class NotificationActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_notification);

        Intent intent = getIntent();
        String body = intent.getStringExtra("info");
        //Log.d("Extras", "X: " + intent.getExtras());

        TextView infoText = this.findViewById(R.id.infoTextView);
        infoText.setText(body);

        findViewById(R.id.approveButton).setOnClickListener(
                new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        //close this activity and returns to login
                        finish();
                    }
                });
    }
}
