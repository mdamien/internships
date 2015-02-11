require 'csv'

desc "Import internships from csv file"

task :import => [:environment] do
  file = "stages.csv"
  internships = []
  CSV.foreach(file, :headers => true) do |row|
    #Data are this way: Automne 2015 => 2015A. We are separating year and semester
    semester = row[7].last(1)
    semesterYear = row[7][0..-1]

    Internship.create({
      id: row[0],
      address: row[1],
      branch: row[2],
      company: row[3],
      description: row[4],
      student: row[5],
      level: row[6],
      semester: semester,
      year: semesterYear,
      subject: row[8],
      teacher: row[9]
    })
  end
end

#num,addresse,branche,company,description,etudiant,niveau,semestre,sujet,tuteur