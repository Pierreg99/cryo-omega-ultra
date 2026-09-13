package examples.integrations;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

/**
 * Minimal Java 11 interoperability example.
 * The gateway must be running locally before this program is executed.
 */
public final class CryoOmegaGatewayExample {
    public static void main(String[] args) throws Exception {
        var uri = URI.create("http://127.0.0.1:8787/api/health");
        var request = HttpRequest.newBuilder(uri).GET().build();
        var response = HttpClient.newHttpClient()
                .send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println("HTTP " + response.statusCode());
        System.out.println(response.body());
    }
}
