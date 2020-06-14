package com.example.vexillum;

import android.app.PendingIntent;
import android.content.Intent;
import android.util.Log;

import androidx.localbroadcastmanager.content.LocalBroadcastManager;

import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;

public class FirebaseService extends FirebaseMessagingService {
    private static final String TAG = "FirebaseService";

    public FirebaseService() {
        Log.d(TAG, "Start");
    }

    @Override
    public void onMessageReceived(RemoteMessage remoteMessage) {
        Log.d(TAG, "From: " + remoteMessage.getFrom());
        Log.d(TAG, "To: " + remoteMessage.getTo());

        if(remoteMessage.getNotification() != null){
            Log.d(TAG, "Notification");

            String click_action = remoteMessage.getNotification().getClickAction();
            Intent intent = new Intent(click_action);
            intent.putExtra("info", remoteMessage.getData().get("info"));
            intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
            PendingIntent pendingIntent = PendingIntent.getActivity(this,
                    0,
                    intent,
                    PendingIntent.FLAG_ONE_SHOT);
            try {
                pendingIntent.send();
            } catch (PendingIntent.CanceledException e) {
                e.printStackTrace();
            }
        }
        else{
            Log.d(TAG, "Data");

            Intent intent = new Intent("data_message");
            intent.putExtra("history", remoteMessage.getData().toString());
            LocalBroadcastManager.getInstance(this).sendBroadcast(intent);
        }
    }

    @Override
    public void onNewToken(String token) {
        Log.d(TAG, "Refreshed token: " + token);
    }
}
