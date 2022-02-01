package fr.univlyon1.bda;

import fr.univlyon1.bda.modele.Tortoise;
import fr.univlyon1.bda.repositories.TortoiseRepository;
import fr.univlyon1.bda.services.TortoiseService;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.*;
import java.net.MalformedURLException;
import java.net.URL;
import java.nio.charset.Charset;

@SpringBootApplication
public class App {

    public static String readAll(Reader rd) throws IOException {
        StringBuilder sb = new StringBuilder();
        int cp;
        while ((cp = rd.read()) != -1) {
            sb.append((char) cp);
        }
        return sb.toString();
    }

    public static JSONObject getData(String url) throws IOException {
        InputStream is = new URL(url).openStream();
        try {
            BufferedReader rd = new BufferedReader(new InputStreamReader(is, Charset.forName("UTF-8")));
            String jsonText = readAll(rd);
            JSONObject json = new JSONObject(jsonText);
            return json;
        } finally {
            is.close();
        }
    }
    public static void main(String[] args) throws IOException {

        TortoiseService ts = new TortoiseService();
        ts.createTortoise(new Tortoise(0,695400,000005454));

        JSONObject jso = getData("http://192.168.77.94/race/large");
        System.out.println(jso.getJSONArray("tortoises").toString());
    }
}
