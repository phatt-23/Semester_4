import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'io.ionic.starter',
  appName: 'http_communication',
  webDir: 'build',
  server: {
    url: 'https://phatt-23.github.io/TAMZ1-http-app',
    cleartext: true
  }
};

export default config;
