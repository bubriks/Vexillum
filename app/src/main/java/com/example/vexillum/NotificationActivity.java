package com.example.vexillum;

import android.content.Intent;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.TimeoutException;

public class NotificationActivity extends AppCompatActivity {

    String QUEUE_NAME = "android_queue";

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
                        SendResponse("1");
                        //close this activity
                        finish();
                    }
                });

        findViewById(R.id.denyButton).setOnClickListener(
                new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        SendResponse("2");
                        //close this activity
                        finish();
                    }
                });

        //should be run on different thread
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();

        StrictMode.setThreadPolicy(policy);
    }

    private void SendResponse(String status) {
        try {
            ConnectionFactory factory = new ConnectionFactory();

            factory.setHost("35.228.252.67");
            factory.setUsername("admin");
            factory.setPassword("admin");
            Connection connection;
            Channel channel;
            connection = factory.newConnection();
            channel = connection.createChannel();

            channel.queueDeclare(QUEUE_NAME, false, false, false, null);
            String message = "{\r\n    \"action\": 2,\r\n\t\"status\": "+status+",\r\n\t\"IotTag\": \"key=c6b9ZKvlWKY:APA91bFb6ErXami15L9qYt3xJeNdYWcj8e3kTgVFLZ2hV30uY0rK5PeR63sUOYxZiBYr9tgnGD8v7LXRvZ1FCPitBypbMbmmpDYawPKI3v7d63-81-1l7stzWezDxczIfBXkr1PThth_\",\r\n\t\"AndroidId\": \"key=c6b9ZKvlWKY:APA91bFb6ErXami15L9qYt3xJeNdYWcj8e3kTgVFLZ2hV30uY0rK5PeR63sUOYxZiBYr9tgnGD8v7LXRvZ1FCPitBypbMbmmpDYawPKI3v7d63-81-1l7stzWezDxczIfBXkr1PThth_\"\r\n}";
            channel.basicPublish("", QUEUE_NAME, null, message.getBytes(StandardCharsets.UTF_8));
            System.out.println(" [x] Sent '" + message + "'");
            channel.close();
            connection.close();
        } catch (IOException | TimeoutException e) {
            throw new RuntimeException("rabbitmq problem", e);
        }
    }
}
