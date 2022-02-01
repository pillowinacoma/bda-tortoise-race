package fr.univlyon1.bda;

import fr.univlyon1.bda.modele.Tortoise;
import fr.univlyon1.bda.repositories.TortoiseRepository;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.io.*;
import java.net.URL;
import java.nio.charset.Charset;
import java.util.stream.Stream;

@SpringBootApplication
  public class App {

    @Value("${spring.datasource.url}")
    String url;
    @Value("${spring.datasource.username}")
    String user;
    @Value("${spring.datasource.password}")
    String password;

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

            SpringApplication.run(App.class, args);

//        JSONObject jso = getData("http://192.168.77.94/race/large");
//        System.out.println(jso.getJSONArray("tortoises").toString());
    }

    @Bean
    ApplicationRunner init(TortoiseRepository tr) {

        String[][] data = {
                {"0", "73", "123"},
                {"1", "73", "100"},
                {"2", "73", "151"}
        };

        return args -> {
            Stream.of(data).forEach(array -> {
                Tortoise tortoise = new Tortoise(
                        Integer.parseInt(array[0]),
                        Integer.parseInt(array[1]),
                        Integer.parseInt(array[3])
                );
                tr.save(tortoise);
            });
            tr.findAll().forEach(System.out::println);
        };
    }

}
