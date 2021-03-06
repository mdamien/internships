class Internship < ActiveRecord::Base
  include Filterable

  scope :from_year, -> (year) { where("year >= ?", year) }
  scope :to_year, -> (year) { where("year <= ?", year) }
  scope :from_semester, -> (from_year, from_semester) { where.not("semester LIKE '%P%' and year = ?", from_year) unless from_semester == 'P' }
  scope :to_semester, -> (to_year, to_semester) { where.not("semester LIKE '%A%' and year = ?", to_year) unless to_semester == 'A' }
  scope :company_like, -> (company) { where("company LIKE ?", "%"+ company + "%") }
  scope :country_like, -> (country) { where("country LIKE ?", "%"+ country + "%") }
  scope :city_like, -> (city) { where("city LIKE ?", "%"+ city + "%") }
  scope :level_like, -> (level) { where("level_abbreviation LIKE ?", "%"+ level + "%") }
  scope :filiere_like, -> (filiere) { where("filiere_abbreviation LIKE ?", "%"+ filiere + "%") }
  scope :branch_like, -> (branch) { where("branch_abbreviation LIKE ?", "%"+ branch + "%") }
  scope :confidential_only, -> { where("confidential = 't'") }
  scope :exclude_not_done, -> { where("done = 't'") }
  scope :company_equal, -> (company) { where("company = ?", + company) }
  scope :branch_not_empty, -> { where.not(branch_abbreviation: '') }

  scope :order_by_semester_desc, -> { order(year: :DESC).order(semester: :ASC) }
  scope :order_by_semester_asc, -> { order(year: :ASC).order(semester: :DESC) }

  # Limit the internship retrieval period between two given semesters.
  # @param from_s[String] Semester from which internships will be retrieved. Format example : "A2015".
  # @param to_s[String] Semester up to which internships will be retrieved. Format example : "A2015".
  def self.from_semester_to_semester(from_s, to_s)
    from_year = from_s[1..4].to_i
    to_year = to_s[1..4].to_i
    from_semester = from_s[0]
    to_semester = to_s[0]

    return from_year(from_year)
               .to_year(to_year)
               .from_semester(from_year, from_semester)
               .to_semester(to_year, to_semester)
  end

  # Order the internships in a specific order used in the table view on the homepage.
  def self.order_internships_for_table
    return order(year: :DESC)
           .order(semester: :ASC)
           .order(country: :ASC)
           .order(company: :ASC)
  end

  # Return internship from the most recent year.
  def self.most_recent_internships
    most_recent_year = Internship.maximum("year")
    return Internship.from_year(most_recent_year)
  end

  # Return an array of internships based on a search query.
  # @param query[Hash] Query containing all the filter attributes. Manage to_semester, from_semester, confidential_only, include_not_done, company_like, country_like, city_like, filiere_like, done_only, branch_like, level_like parameters.
  def self.search query
    if query.has_key?(:from_semester) && query.has_key?(:to_semester)
      internships = from_semester_to_semester(query[:from_semester], query[:to_semester])
      internships = internships.confidential_only if query[:confidential_only].present?
      internships = internships.exclude_not_done unless query[:include_not_done].present?

      # Filtering internships with query parameters values.
      internships = internships.filter(query.slice(:company_like, :country_like, :city_like, :filiere_like, :done_only, :branch_like, :level_like))

      return internships
    end

    # Returning most recent internships if missing parameters.
    return most_recent_internships
  end

  # Return an array containing for each semester and branch a count of internships found in DB.
  # @param query[Hash] Query containing all the filter attributes. Manage to_semester, from_semester, confidential_only, include_not_done, company_like, country_like, city_like, filiere_like, done_only, branch_like, level_like parameters.
  # @return [Hash<Array, Integer>] Item format example: [2010, "P", "GI"]: 53
  def self.internship_count_by_semester query
    internships = search(query)

    internships = internships
                      .branch_not_empty
                      .group("year")
                      .group("semester")
                      .group("branch_abbreviation")
                      .order_by_semester_asc
                      .count

    return internships
  end

  # @return [Array<Internship>] Each internship has a year property. Internships are ordered by year.
  def self.all_internship_years
    return select(:year).distinct.order(year: :ASC)
  end

  # @return [Array<Internship>] Each internship has a branch_abbreviation property. Internships are ordered by branch_abbreviation ASC.
  def self.all_branches
    return select(:branch_abbreviation).branch_not_empty.distinct.order(branch_abbreviation: :ASC)
  end

  # @return [Array<String>] Array of all branch abbreviations ordered by branch abbreviation ASC.
  def self.all_branches_for_select
    return self.all_branches.map { |b| b.branch_abbreviation }
  end

  # Return all filiere abbreviations in the database, grouped by branch in a Hash. Hash keys are ordered by branch abbreviation.
  # @return [Hash<String, Array>] Item format example: "GI": ["FDD", "ICSI"]
  def self.all_filieres
    # Grouping and having because some students from branches took filieres from other branches (very rare, so having count > 5 is enough to make sure we select only actual branch filieres)
    filieres =  select(:branch_abbreviation)
                    .select(:filiere_abbreviation)
                    .branch_not_empty
                    .where.not(filiere_abbreviation: '')
                    .group(:branch_abbreviation)
                    .group(:filiere_abbreviation)
                    .distinct
                    .order(branch_abbreviation: :ASC)
                    .order(filiere_abbreviation: :ASC)
                    .having("COUNT (*) > 5")

    # Filieres that any student from any branch can choose.
    filieres_data = {
        "Transversales" => ["Libre", "MPI"]
    }

    filieres.each do |f|
      if filieres_data.has_key?(f.branch_abbreviation)
        filieres_data[f.branch_abbreviation].push(f.filiere_abbreviation)
      else
        filieres_data[f.branch_abbreviation] = [f.filiere_abbreviation]
      end
    end

    return filieres_data
  end

  def self.all_levels
    return select(:level_abbreviation).where.not(level_abbreviation: '').distinct.order(level_abbreviation: :ASC)
  end

  def self.all_levels_for_select
    return self.all_levels.map { |l| l.level_abbreviation }
  end

  def self.all_semesters_ordered
    semesters_in_database = select(:year).select(:semester).distinct.group("year").group("semester").order_by_semester_desc

    # Semesters will be sorted already, as we already sorted the data from the database.
    semesters = Array.new

    semesters_in_database.each do |s|
      semesters.push(s.semester + s.year.to_s)
    end

    return semesters
  end

  def self.all_countries_ordered_for_select
    return  select(:country).distinct.order(country: :ASC).map { |c| c.country }
  end

  def self.all_cities_grouped_by_country_for_select
    cities = select(:country)
        .select(:city)
        .where.not(city: '')
        .where.not("trim(city) LIKE ?", "(%")
        .distinct
        .order(country: :ASC)
        .order(city: :ASC)

    cities_data = Hash.new

    cities.each do |c|
      if cities_data.has_key?(c.country)
        cities_data[c.country].push(c.city)
      else
        cities_data[c.country] = [c.city]
      end
    end

    return cities_data
  end

  def self.top_companies query
    internships = search(query)

    top_companies = internships.select("upper(company)").group("upper(company)").order("count_company DESC").limit(20).count(:company)
    companies = top_companies.map { |c| c[0] }
    return internships.where("upper(company) IN (?)", companies)
                     .group("year")
                     .group("semester")
                     .group("upper(company)")
                     .order_by_semester_asc
                     .count,
        top_companies
  end
end