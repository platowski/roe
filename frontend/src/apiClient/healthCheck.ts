import {client} from "./backendClient";
export async function getHealthCheck() {
    return client.get("/health_check");
}