package com.example.vexillum.ui.home;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class HomeViewModel extends ViewModel {

    //todo maybe should not be static
    private static MutableLiveData<String> mText;

    public HomeViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("This is home fragment");
    }

    public void setText(String text){
        mText.setValue(text);
    }

    public LiveData<String> getText() {
        return mText;
    }
}