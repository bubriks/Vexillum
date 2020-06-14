package com.example.vexillum.ui.home;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class HomeViewModel extends ViewModel {

    //todo maybe should not be static
    private static MutableLiveData<String> mText = new MutableLiveData<>();

    public void setText(String text){
        mText.setValue(text);
    }

    public LiveData<String> getText() {
        return mText;
    }
}