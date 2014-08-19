class main:
	
	def __init_(self, alg_actor_ranker, alg_movie_predictor, movie_bdd):
		self.alg_person_ranker = actor_ranker
		self.alg_movie_predictor = alg_movie_predictor
		self.movie_bdd = movie_bdd
		self.trained = False # boolean
	
	
	def train(self):
		
		# acquire the revelant list of persons that played in all the movies that are part of the database.
		movie_persons = self._getTotalMovieInformations()
		
		for persons in movie_persons:
			
			# feed each person to the person ranker class instance.
			# we pass his id, the movies he played in as well as the status that he held during the making.
			
			for person, status in persons:
				
				# we extract the previous movies the current person has been related to.
				filmography = self.movie_bdd.extractMoviesFromPersonId(person, status)
				
				# we feed this information to the 'person ranker' for training purposes.
				self.alg_person_ranker.train(person, status, filmography)
			
		
		# the person ranking is now over.
		# the next step is to train the movie predictor.
		
		for persons in movie_persons:
			
			persons_scores = []
			
			for person, status in persons:
				
				person_score = self.alg_person_ranker.getPersonScore(person, status)
				persons_scores.append( person_score )
				
				
			self.alg_movie_predictor.train(persons_scores)
			
		# training complete
		self.trained = True
		
		return
		
	
	
	def _getTotalMovieInformations(self):
		
		movie_persons = []
		
		# this is the variable that will hold the current movie index.
		movie_id = 0
		
		n_movies_in_bdd = self.movie_bdd.getTotalMovieCount()
		
		while (movie_id < n_movies_in_bdd):
		
			persons = self.movie_bdd.extractPersonsFromMovieId(movie_id)
							
			movie_persons.append( persons )
				
		return movie_persons
				
	
	
	
	def predictMovieScore(self, movie_title):
		
		if (not self.trained):
			return -1
		
		# first part: get the necessary informations
		
		# get movie id (if it exists)
		movie_id = self.movie_bdd.getMovieIdFromTitleName(movie_title)
		
		if (movie_id < 0):
			# the movie couldn't be found
			return -1
			
		
		persons = self.movie_bdd.extractPersonsFromMovieId(movie_id)
		
		for person in persons:
			
		
			
			
		# now that we have the movie id we can extract all the relevant informations
		# that we need for the prediction process.
		
		# get the director
		director = movie_bdd.getDirectorFromMovieId(movie_id)
		
		# get the actors
		actors = movie_bdd.getActorsFromMovieId(movie_id)
		
		# get the producers
		producers = movie_bdd.getProducersFromMovieId(movie_id)
		
		# get the writers
		writers = movie_bdd.getWritersFromMovieId(movie_id)
		
		# get the movie budget
		budget = movie_bdd.getBudgetFromMovie(movie_id)
		
		# second part: get the score of each of the persons associated with the cinematographic project:
		
		actors_score = []
		producers_score = []
		writers_score = []
		director_score = []
		
		
		for i in range(len(actors)):
			actors_score.append(self.alg_person_ranker.getActorRanking(actors[i]))
			
		for i in range(len(producers)):
			producers_score.append(self.alg_person_ranker.getProducerRanking(producer[i]))
			
		for i in range(len(writers)):
			writers_score.append(self.alg_person_ranker.getWriterRanking(writers[i]))
		
		director_score = [ self.alg_person_ranker.getDirectorRanking(director) ]
		
		# construct the dictionary that will be passed as argument to the prediction instance
		
		movie_attributes = {}
		movie_attributes['director'] = 	director
		movie_attributes['producers'] = producers
		movie_attributes['writers'] = 	writers
		movie_attributes['budget'] = 	budget
		movie_attributes['actors'] = 	actors
		
		# third part: predict the movie's rating based on the persons and the budget
		
		movie_score = self.alg_movie_predictor(movie_attributes)
		
		return movie_score
