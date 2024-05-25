package net.keimag.hakoirimusume;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import okhttp3.*;

import java.io.File;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.io.IOException;
import java.io.InputStream;
import java.io.UncheckedIOException;
import java.net.http.HttpRequest;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.function.Supplier;

public class ImgurAnonymousUploader {
    private final String imgurClientId;
    private final OkHttpClient okHttpClient = new OkHttpClient();
    private final ObjectMapper mapper = new ObjectMapper();

    public ImgurAnonymousUploader(String imgurClientId) {
        this.imgurClientId = imgurClientId;

    }

    public Map<String, Object> upload(byte[] image, String filename, String title, String description) throws IOException {

        RequestBody requestBody = new MultipartBody.Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart("image", filename, RequestBody.create(image))
                .addFormDataPart("type", "image")
                .addFormDataPart("title", title)
                .addFormDataPart("description", description)
                .build();
        Request request = new Request.Builder()
                .url("https://api.imgur.com/3/image")
                .header("Authorization", "Client-ID " + imgurClientId)
                .post(requestBody)
                .build();
        try (Response response = okHttpClient.newCall(request).execute()) {
            Map<String, Object> map = mapper.readValue(String.valueOf(response.body()), Map.class);
            return map;
        }
    }

    public Map<String, Object> uploadFile(File file, String title, String description) throws IOException {
        byte[] image = Files.readAllBytes(file.toPath());
        String filename = file.toPath().getFileName().toString();
        System.out.println(filename);
        return upload(image, filename, title, description);
    }
}
