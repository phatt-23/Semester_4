CREATE TABLE "user" (
  "user_id" bigint GENERATED AS IDENTITY PRIMARY KEY,
  "username" nvarchar(20) UNIQUE NOT NULL,
  "first_name" nvarchar(50) NOT NULL,
  "last_name" nvarchar(50) NOT NULL,
  "email" nvarchar(255) UNIQUE NOT NULL,
  "registration_date" datetime DEFAULT GETDATE(),
  "about_me" nvarchar(500),
  "profile_picture_id" bigint,
  "last_login" datetime,
  "status" nvarchar2(255) NOT NULL CHECK ("status" IN ('active', 'banned', 'suspended')),
  "is_deleted" bit DEFAULT 0
);

CREATE TABLE "channel" (
  "channel_id" bigint GENERATED AS IDENTITY PRIMARY KEY,
  "user_id" bigint,
  "channel_name" nvarchar(50) UNIQUE NOT NULL,
  "description" nvarchar(1000),
  "pfp_media_id" bigint,
  "banner_media_id" bigint,
  "creation_date" datetime NOT NULL DEFAULT GETDATE(),
  "is_deleted" bit DEFAULT 0
);

CREATE TABLE "media" (
  "media_id" bigint GENERATED AS IDENTITY PRIMARY KEY,
  "url" nvarchar(1000) UNIQUE NOT NULL,
  "type" nvarchar(50) NOT NULL,
  "upload_date" datetime DEFAULT GETDATE()
);

CREATE TABLE "video" (
  "video_id" bigint GENERATED AS IDENTITY PRIMARY KEY,
  "channel_id" bigint,
  "thumbnail_id" bigint,
  "video_file_id" bigint,
  "visibility" nvarchar2(255) NOT NULL CHECK ("visibility" IN ('private', 'unlisted', 'public', 'draft')) DEFAULT 'public',
  "is_monetized" bit DEFAULT 1,
  "is_deleted" bit DEFAULT 0,
  "title" nvarchar(255) NOT NULL,
  "description" nvarchar(1000),
  "upload_date" datetime NOT NULL DEFAULT GETDATE(),
  "duration" bigint NOT NULL,
  "view_count" integer NOT NULL,
  "like_count" integer NOT NULL,
  "dislike_count" integer NOT NULL,
  "comment_count" integer NOT NULL
);

CREATE TABLE "playlist" (
  "playlist_id" bigint GENERATED AS IDENTITY PRIMARY KEY,
  "user_id" bigint,
  "title" nvarchar(255) NOT NULL,
  "visibility" nvarchar2(255) NOT NULL CHECK ("visibility" IN ('private', 'unlisted', 'public', 'draft')) DEFAULT 'public',
  "creation_date" datetime NOT NULL DEFAULT GETDATE(),
  "is_deleted" bit DEFAULT 0
);

CREATE TABLE "playlist_video" (
  "playlist_id" bigint,
  "video_id" bigint,
  "added_date" datetime NOT NULL DEFAULT GETDATE(),
  "order" integer,
  PRIMARY KEY ("playlist_id", "video_id")
);

CREATE TABLE "comment" (
  "comment_id" bigint GENERATED AS IDENTITY PRIMARY KEY,
  "parent_comment_id" bigint,
  "user_id" bigint,
  "video_id" bigint,
  "content" nvarchar(500) NOT NULL,
  "comment_date" datetime NOT NULL DEFAULT GETDATE(),
  "edited_date" datetime,
  "is_deleted" bit DEFAULT 0
);

CREATE TABLE "reaction" (
  "reaction_id" bigint GENERATED AS IDENTITY PRIMARY KEY,
  "user_id" bigint,
  "video_id" bigint,
  "comment_id" bigint,
  "reaction_type" nvarchar2(255) NOT NULL CHECK ("reaction_type" IN ('like', 'dislike')) NOT NULL,
  "reaction_date" datetime NOT NULL DEFAULT GETDATE()
);

CREATE TABLE "subscription" (
  "subscriber_id" bigint,
  "channel_id" bigint,
  "notification_preference" bit DEFAULT 1,
  "subscription_date" datetime NOT NULL DEFAULT GETDATE(),
  PRIMARY KEY ("subscriber_id", "channel_id")
);

CREATE TABLE "video_view" (
  "video_view_id" bigint GENERATED AS IDENTITY PRIMARY KEY,
  "user_id" bigint,
  "video_id" bigint,
  "view_date" datetime NOT NULL DEFAULT GETDATE(),
  "duration_watched" bigint NOT NULL
);

CREATE TABLE "video_category" (
  "video_id" bigint,
  "category_id" bigint,
  PRIMARY KEY ("video_id", "category_id")
);

CREATE TABLE "category" (
  "category_id" bigint GENERATED AS IDENTITY PRIMARY KEY,
  "parent_category_id" bigint,
  "category_name" nvarchar(50) UNIQUE NOT NULL
);

CREATE TABLE "advertisement" (
  "advertisement_id" bigint GENERATED AS IDENTITY PRIMARY KEY,
  "media_id" bigint,
  "title" nvarchar(255) NOT NULL,
  "content" nvarchar(255) NOT NULL,
  "cta_link" nvarchar(1000),
  "target_audience" nvarchar(500) NOT NULL,
  "status" nvarchar2(255) NOT NULL CHECK ("status" IN ('active', 'inactive', 'expired')) DEFAULT 'active',
  "click_rate" float NOT NULL,
  "revenue" MONEY NOT NULL,
  "budget" MONEY NOT NULL,
  "created_date" datetime NOT NULL DEFAULT GETDATE(),
  "last_updated" datetime NOT NULL DEFAULT GETDATE()
);

CREATE TABLE "video_advertisement" (
  "video_ad_id" bigint GENERATED AS IDENTITY PRIMARY KEY,
  "video_id" bigint,
  "advertisement_id" bigint,
  "start_time" integer NOT NULL,
  "end_time" integer NOT NULL
);

CREATE TABLE "ad_event" (
  "event_id" bigint GENERATED AS IDENTITY PRIMARY KEY,
  "video_id" bigint,
  "advertisement_id" bigint,
  "user_id" bigint,
  "event_type" nvarchar2(255) NOT NULL CHECK ("event_type" IN ('impression', 'click', 'view', 'conversion')) NOT NULL,
  "event_timestamp" datetime NOT NULL DEFAULT GETDATE(),
  "duration_watched" integer
);

ALTER TABLE "user" ADD FOREIGN KEY ("profile_picture_id") REFERENCES "media" ("media_id");

ALTER TABLE "channel" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("user_id");

ALTER TABLE "channel" ADD FOREIGN KEY ("pfp_media_id") REFERENCES "media" ("media_id");

ALTER TABLE "channel" ADD FOREIGN KEY ("banner_media_id") REFERENCES "media" ("media_id");

ALTER TABLE "video" ADD FOREIGN KEY ("channel_id") REFERENCES "channel" ("channel_id");

ALTER TABLE "video" ADD FOREIGN KEY ("thumbnail_id") REFERENCES "media" ("media_id");

ALTER TABLE "video" ADD FOREIGN KEY ("video_file_id") REFERENCES "media" ("media_id");

ALTER TABLE "playlist" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("user_id");

ALTER TABLE "playlist_video" ADD FOREIGN KEY ("playlist_id") REFERENCES "playlist" ("playlist_id");

ALTER TABLE "playlist_video" ADD FOREIGN KEY ("video_id") REFERENCES "video" ("video_id");

ALTER TABLE "comment" ADD FOREIGN KEY ("comment_id") REFERENCES "comment" ("parent_comment_id");

ALTER TABLE "comment" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("user_id");

ALTER TABLE "comment" ADD FOREIGN KEY ("video_id") REFERENCES "video" ("video_id");

ALTER TABLE "reaction" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("user_id");

ALTER TABLE "reaction" ADD FOREIGN KEY ("video_id") REFERENCES "video" ("video_id");

ALTER TABLE "reaction" ADD FOREIGN KEY ("comment_id") REFERENCES "comment" ("comment_id");

ALTER TABLE "subscription" ADD FOREIGN KEY ("subscriber_id") REFERENCES "user" ("user_id");

ALTER TABLE "subscription" ADD FOREIGN KEY ("channel_id") REFERENCES "channel" ("channel_id");

ALTER TABLE "video_view" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("user_id");

ALTER TABLE "video_view" ADD FOREIGN KEY ("video_id") REFERENCES "video" ("video_id");

ALTER TABLE "video_category" ADD FOREIGN KEY ("video_id") REFERENCES "video" ("video_id");

ALTER TABLE "video_category" ADD FOREIGN KEY ("category_id") REFERENCES "category" ("category_id");

ALTER TABLE "category" ADD FOREIGN KEY ("category_id") REFERENCES "category" ("parent_category_id");

ALTER TABLE "advertisement" ADD FOREIGN KEY ("media_id") REFERENCES "media" ("media_id");

ALTER TABLE "video_advertisement" ADD FOREIGN KEY ("video_id") REFERENCES "video" ("video_id");

ALTER TABLE "video_advertisement" ADD FOREIGN KEY ("advertisement_id") REFERENCES "advertisement" ("advertisement_id");

ALTER TABLE "ad_event" ADD FOREIGN KEY ("video_id") REFERENCES "video" ("video_id");

ALTER TABLE "ad_event" ADD FOREIGN KEY ("advertisement_id") REFERENCES "advertisement" ("advertisement_id");

ALTER TABLE "ad_event" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("user_id");


