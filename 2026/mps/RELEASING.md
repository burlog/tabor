# Releasing MPS to Google Play

The app is published as `cz.burlog.tabor.mps`.

## 1. Create the upload keystore (once)

```bash
keytool -genkey -v -keystore mps-upload.jks \
  -keyalg RSA -keysize 2048 -validity 10000 -alias mps
```

Keep `mps-upload.jks` and its passwords safe. The keystore is git-ignored
(`*.jks`) and must never be committed. Storing it in a password manager and a
secure backup is recommended.

## 2. Build a signed release bundle

Release signing is configured entirely from environment variables, so no
secret is ever written to disk or committed.

| Variable             | Required | Default          |
| -------------------- | -------- | ---------------- |
| `MPS_STORE_PASSWORD` | yes      | —                |
| `MPS_STORE_FILE`     | no       | `mps-upload.jks` |
| `MPS_KEY_ALIAS`      | no       | `mps`            |
| `MPS_KEY_PASSWORD`   | no       | `MPS_STORE_PASSWORD` |

Build the Android App Bundle (note the leading space to keep the password out
of shell history when `HISTCONTROL=ignorespace`):

```bash
 MPS_STORE_PASSWORD='your-keystore-password' ./gradlew bundleRelease
```

Output: `app/build/outputs/bundle/release/app-release.aab`

Without `MPS_STORE_PASSWORD`, `bundleRelease` still succeeds but the bundle is
unsigned (useful for local checks only).

## 3. Upload to Play Console

1. Create the app in the Play Console and enroll in **Play App Signing**
   (Google manages the release key; `mps-upload.jks` becomes the upload key).
2. Upload the `.aab` to a track: start with **Internal testing**, then promote
   to Closed / Open / Production.
3. Complete the store listing, content rating, and **Data safety** form. The
   app requests fine/coarse location, so its use must be declared there and in
   the privacy policy.

## 4. Updates

Bump `versionCode` (and usually `versionName`) in `app/build.gradle.kts` for
every new upload; Play rejects duplicate version codes.
