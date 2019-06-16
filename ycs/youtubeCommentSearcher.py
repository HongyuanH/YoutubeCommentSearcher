import googleapiclient.discovery

class YoutubeCommentSearcher():
	def __init__(self, playlistId, developerKey):
		self.playlistId = playlistId
		self.developerKey = developerKey
		self.api = googleapiclient.discovery.build(
			"youtube", "v3", developerKey=self.developerKey)
	
	def getPlaylistItems(self, playlistId, pageToken=""):
		request = self.api.playlistItems().list(
			playlistId=playlistId,
			pageToken=pageToken,
			part="snippet"
		)
		return request.execute()

	def getCommentThreads(self, videoId, pageToken=""):
		request = self.api.commentThreads().list(
			videoId=videoId,
			pageToken=pageToken,
			part="snippet,replies"
		)
		return request.execute()
		
	def getAllVideoIds(self):
		videoIds = []
		# the first page
		response = self.getPlaylistItems(self.playlistId)
		for item in response["items"]:
			videoIds.append(item["snippet"]["resourceId"]["videoId"])
		# the remaining pages
		while "nextPageToken" in response:
			nextPageToken = response["nextPageToken"]
			response = self.getPlaylistItems(self.playlistId, nextPageToken)
			for item in response["items"]:
				videoIds.append(item["snippet"]["resourceId"]["videoId"])
		return videoIds
		
	def getAllComments(self, videoId):
		comments = []
		# the first page
		response = self.getCommentThreads(videoId)
		for item in response["items"]:
			topLevelComment = item["snippet"]["topLevelComment"]
			author = topLevelComment["snippet"]["authorDisplayName"]
			link = topLevelComment["snippet"]["videoId"]
			text = topLevelComment["snippet"]["textOriginal"]
			time = topLevelComment["snippet"]["updatedAt"]
			comments.append("[%s][%s][%s]%s" % (link, author, time, text))
		# the remaining pages
		while "nextPageToken" in response:
			nextPageToken = response["nextPageToken"]
			response = self.getCommentThreads(videoId, nextPageToken)
			for item in response["items"]:
				topLevelComment = item["snippet"]["topLevelComment"]
				author = topLevelComment["snippet"]["authorDisplayName"]
				link = topLevelComment["snippet"]["videoId"]
				text = topLevelComment["snippet"]["textOriginal"]
				time = topLevelComment["snippet"]["updatedAt"]
				comments.append("[%s][%s][%s]%s" % (link, author, time, text))
		return comments
