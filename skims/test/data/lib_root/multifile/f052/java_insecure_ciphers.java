package com.gree.encryption.services;

import com.gree.airconditioner.GreeAirconditionerDevice;
import com.gree.airconditioner.binding.GreeDeviceBinderService;
import com.gree.airconditioner.binding.GreeDeviceBinding;

public class GreeEncryptionService {

    private final GreeDeviceBinderService binderService;
    private final GreeCommunicationService communicationService;

    public void getAlgo(String cipher) {
        if (cipher){
            return "MD5";
        } else {
            return "SHA256";
        }
    }
}
