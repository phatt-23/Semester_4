# Form Description:

- Upload of a new video.

1. Select a user for which to add the video.
2. Choose one of the his channels to which to add the video.
3. Input details - title, description, visibility, monetization
    (setting monetization to false will disable addition of ads to the video)
4. Upload a thumbnail and the video file.
5. Choose playlists to which to add the video.
6. Choose categories to which to add the video.
7. Search advertisements by title or (and) content. Choose one and specify where to put it into the video.
8. Segment the video into video chapters.
9. Submit the video upload.


# Functions:
1. fn GetUsersByName(searchUsername: String) -> List<User>
2. fn GetUserById(userId: Integer) -> User
3. fn GetChannelsFromUser(userId: Integer) -> List<Channel>
4. fn GetChannelById(channelId: Integer) -> Channel

5. fn UploadThumbnailFile(filepath: String) -> Media 
6. fn UploadVideoFile(filepath: String) -> Media 

7. fn AddVideoChapter(videoId: Integer, title: String, startTime: Integer, endTime: Integer)
8. fn RemoveVideoChapter(videoChapterId: Integer)

9. fn GetVideoCategoriesByName(categoryName: String) -> List<Categories>
10. fn AddVideoCategory(categoryId: Integer)
11. fn RemoveVideoCategory(categoryId: Integer)

12. fn GetChannelPlaylists(channelId: Integer) -> List<Playlist>
13. fn AddVideoToPlaylist(playlistId: Integer) 
14. fn RemoveVideoFromPlaylist(playlistId: Integer)

15. fn GetAdvertisementsByName(searchAdName: String) -> List<Advertisement>
16. fn AddVideoAdvertisement(advertisementId: Integer, time: Integer)
17. fn RemoveVideoAdvertisement(videoAdvertisementId: Integer)

18. fn FinishVideoUpload()


-- transaction to add a video
-- assign channel (trivial)
-- assign categories (non-trivial, working with video_category, possibly creating new categories)
-- link video_advertisement(s) (non-trivial, creating new records in video_advertisement)


-- upload a video
-- set:
--      title, 
--      description, 
--      visibility,
--      add_tags (categories)
--      add_comment (first creator's comment)
--      add_into_playlist
--      upload_thumbnail
--      add_advertisement (with timestamps)


create or replace procedure P_UploadVideo(
    p_thumbnail_file    media.media_id%TYPE,
    p_video_file        media.media_id%TYPE,
    visibility          video.visibility%TYPE,
    channel_id          channel.channel_id%TYPE,
    playlist_video_id   playlist_video.playlist_video_id%TYPE,
    subtitle_id         subtitle.subtitle_id%TYPE,
) is
begin
    
end

insert into video_category(video_id, category_id)
values ()  
  "video_id" bigint,
  "category_id" bigint,

