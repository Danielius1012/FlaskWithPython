import pypyodbc

class Client(object):
    def __init__(self):
        __connectionString = 'Driver={SQL Server Native Client 11.0};Server=tcp:<NAME>.database.windows.net,1433;Database=<DB_NAME>;Uid=<UID>;Pwd=<PWD>;Encrypt=yes;TrustServerCertificate=no;'
        self.connection = pypyodbc.connect(__connectionString)
        self.cursor = self.connection.cursor()
        return;

    def saveQuestion(self, title, question, answer):
        sql = "INSERT INTO Questions(QuestionName, Description, CorrectAnswer, CategoryID) VALUES (?,?,?,?)";
        values = [title, question, answer, 1];
        self.cursor.execute(sql, values);
        self.connection.commit();
        self.connection.close();
        return;

    def getQuestion(self, title):
        sql = "SELECT Description FROM Questions WHERE QuestionName = ?";
        values = [title];
        self.cursor.execute(sql, values);
        results = self.cursor.fetchone();
        question = results[0];
        self.connection.close();
        return question;

    def getAnswer(self, title):
        sql = "SELECT CorrectAnswer FROM Questions WHERE QuestionName = ?";
        values = [title];
        self.cursor.execute(sql, values);
        results = self.cursor.fetchone();
        correctAnswer = results[0];
        self.connection.close();
        return correctAnswer;    
