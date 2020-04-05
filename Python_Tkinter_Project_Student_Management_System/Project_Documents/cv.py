CREATE_SCHEMA = """
CREATE SCHEMA IF NOT EXISTS `mydb`;
"""


CREATE_STUDENT_TABLE = """
CREATE TABLE IF NOT EXISTS `mydb`.`Student` (
  `Student_Number` VARCHAR(45) NOT NULL,
  `StudentFirstName` VARCHAR(45) NOT NULL,
  `StudentLastName` VARCHAR(45) NULL,
  `StudentEmail` VARCHAR(45) NOT NULL,
  `StudentProgram` VARCHAR(45) NOT NULL,
  `StudentDateofJoin` VARCHAR(45) NOT NULL,
  `StudentTerm` INT NOT NULL,
  CHECK (`StudentTerm` >= 1 and `StudentTerm` <= 4),
  `StudentGPA` FLOAT NULL,
  
  CHECK( ((`StudentTerm`=1 and `StudentGPA`=0) or 
        
		 (`StudentTerm`>1 and `StudentGPA`>0)) and 
        
		 (`StudentGPA` <= 4) and (`StudentTerm` <=4)), 
        
UNIQUE INDEX `studentID_UNIQUE` (`Student_Number`),
PRIMARY KEY (`Student_Number`));
"""

CREATE_COURSE_TABLE = """
CREATE TABLE IF NOT EXISTS `mydb`.`Course` (
  `Course_ID` VARCHAR(45) NOT NULL,
  `CourseName` VARCHAR(45) NULL,
  UNIQUE INDEX `courseID_UNIQUE` (`Course_ID`),
  PRIMARY KEY (`Course_ID`));
"""

CREATE_PROFESSOR_TABLE = """
CREATE TABLE IF NOT EXISTS `mydb`.`Professor` (
  `Professor_ID` VARCHAR(45) NOT NULL,
  `ProfessorFirstName` VARCHAR(45) NOT NULL,
  `ProfessorLastName` VARCHAR(45) NOT NULL,
  `ProfessorEmail` VARCHAR(45) NOT NULL,
  UNIQUE INDEX `professorID_UNIQUE` (`Professor_ID`),
  PRIMARY KEY (`Professor_ID`));
"""

CREATE_USERNAME_AND_PASSWORD_TABLE = """

CREATE TABLE IF NOT EXISTS `mydb`.`UsernameAndPassword`(
  `username` VARCHAR(45) NOT NULL,
  `typeOfUser` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NULL,
  UNIQUE INDEX `username_UNIQUE` (`username`),
  CHECK (`typeOfUser` in ('Admin','Professor','Student')),
  PRIMARY KEY (`username`, `typeOfUser`)
  
);
"""

CREATE_GRADE_TABLE = """
CREATE TABLE IF NOT EXISTS `mydb`.`grade` (
  `Student_Number` VARCHAR(45) NOT NULL,
  `Course_ID` VARCHAR(45) NOT NULL,
  `Professor_Professor_ID` VARCHAR(45) NOT NULL,
  `grade` INT NULL,
  
  PRIMARY KEY (`Student_Number`, `Course_ID`),
  
  CONSTRAINT `checker` CHECK (grade >=0 and grade <=100),
  
  CONSTRAINT `fk_grade_Student`
    FOREIGN KEY (`Student_Number`)
    REFERENCES `mydb`.`Student` (`Student_Number`)
    ON DELETE RESTRICT,
    
  CONSTRAINT `fk_grade_Professor1`
    FOREIGN KEY (`Professor_Professor_ID`)
    REFERENCES `mydb`.`Professor` (`Professor_ID`)
    ON DELETE RESTRICT,
    
  CONSTRAINT `fk_grade_Course1`
    FOREIGN KEY (`Course_ID`)
    REFERENCES `mydb`.`Course` (`Course_ID`)
    ON DELETE RESTRICT
    
    );
"""