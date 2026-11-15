# Links the first mention of another reviewed film, and of a director who has
# a page (_plugins/library_pages.rb), inside each review's text. It runs on the
# converted HTML at build time, so the files in _posts/ are never edited and
# the words stay exactly as written: matches are only wrapped in <a>.
#
# Rules
# - Whole titles only, case-sensitive, on word boundaries; longest first.
# - A review never links to itself (title or a.k.a.).
# - Nothing inside existing links, headings, code or tag attributes.
# - "Weak" titles that could be ordinary words ("Prey", "Voices", "Schizo",
#   "Frogs", "Amuck!", or "The" + one word) link only when written as a
#   title: in italics, or followed by the film's year in brackets, or
#   capitalised mid-sentence. A title followed by a different year is a
#   different film and is never linked.
# - Alternative titles link only when multi-word and not shared by another
#   review.
#
# Set PSYCHOTRONIC_NO_AUTOLINK=1 to build without it (for comparing output).
module PsychotronicReviewLinks
  SKIP_TAGS = %w[a h1 h2 h3 h4 h5 h6 code pre script style].freeze
  APOSTROPHE = "(?:'|&rsquo;|&#8217;|’)".freeze
  WEAK_SECOND_WORDS = /\A(?:the|a|an)\s+\S+\z/i

  Target = Struct.new(:text, :url, :year, :weak, :key, keyword_init: true)

  def self.weak?(text)
    words = text.gsub(/[^\p{L}\p{N}'\s]/, "").split
    words.size <= 1 || text.match?(WEAK_SECOND_WORDS)
  end

  def self.akas(value)
    value.to_s.split(%r{\s+/\s+|;\s*}).map(&:strip).reject(&:empty?)
  end

  def self.pattern(text)
    escaped = Regexp.escape(text.gsub("&", "&amp;"))
    escaped = escaped.gsub("'", APOSTROPHE).gsub("’", APOSTROPHE)
    escaped = escaped.gsub("\\ ", "\\s+") # a source line break can fall inside a title
    lead = text.match?(/\A[\p{L}\p{N}]/) ? '(?<![\p{L}\p{N}])' : ""
    tail = text.match?(/[\p{L}\p{N}]\z/) ? '(?![\p{L}\p{N}])' : ""
    Regexp.new("#{lead}#{escaped}#{tail}")
  end

  def self.targets(site)
    posts = site.posts.docs
    titles = posts.map { |p| p.data["title"].to_s }
    aka_counts = Hash.new(0)
    posts.each { |p| akas(p.data["aka"]).each { |a| aka_counts[a.downcase] += 1 } }
    list = []
    posts.each do |p|
      title = p.data["title"].to_s
      next if title.empty?
      list << Target.new(text: title, url: p.url, year: p.data["year"].to_s, weak: weak?(title), key: p.url)
      akas(p.data["aka"]).each do |a|
        next if weak?(a) || aka_counts[a.downcase] > 1 || titles.any? { |t| t.casecmp?(a) }
        list << Target.new(text: a, url: p.url, year: p.data["year"].to_s, weak: false, key: p.url)
      end
    end
    pages = (site.data["library_pages"] || {})["director"] || {}
    pages.each do |name, url|
      next if name.include?("(as ")
      list << Target.new(text: name, url: url, year: "", weak: false, key: url)
    end
    list.sort_by { |t| -t.text.length }
  end

  def self.sentence_start?(before)
    stripped = before.rstrip
    stripped.empty? || stripped.match?(/(?:[.!?:]|&rdquo;|&ldquo;|&lsquo;|["“‘(])\z/)
  end

  def self.link(html, own_url, targets, baseurl)
    used = {}
    tokens = html.split(/(<[^>]+>)/)
    skip_depth = 0
    em_depth = 0
    tokens.each_with_index do |tok, i|
      if tok.start_with?("<")
        name = tok[%r{\A</?\s*([a-zA-Z0-9]+)}, 1].to_s.downcase
        closing = tok.start_with?("</")
        skip_depth += (closing ? -1 : 1) if SKIP_TAGS.include?(name) && !tok.end_with?("/>")
        em_depth += (closing ? -1 : 1) if %w[em i cite].include?(name)
        next
      end
      next if skip_depth.positive? || tok.strip.empty?
      text = tok
      spans = []
      targets.each do |t|
        next if t.key == own_url || used[t.key]
        re = pattern(t.text)
        pos = 0
        while (m = re.match(text, pos))
          pos = m.end(0)
          next if spans.any? { |s| m.begin(0) < s[1] && m.end(0) > s[0] }
          year_after = text[m.end(0)..][/\A\s*\((\d{4})\)/, 1]
          next if year_after && !t.year.empty? && year_after != t.year
          if t.weak && em_depth.zero? && year_after != t.year
            before = text[0...m.begin(0)]
            # A run's first word follows a tag; only inline formatting
            # (not a paragraph or line start) makes that mid-sentence.
            at_run_start = before.strip.empty?
            inline_before = i.positive? && tokens[i - 1].match?(%r{\A</(?:strong|b|span|a)>})
            next if at_run_start ? !inline_before : sentence_start?(before)
          end
          spans << [m.begin(0), m.end(0), t.url]
          used[t.key] = true
          break
        end
      end
      next if spans.empty?
      out = +""
      cursor = 0
      spans.sort_by(&:first).each do |from, to, url|
        out << text[cursor...from] << %(<a class="autolink" href="#{baseurl}#{url}">#{text[from...to]}</a>)
        cursor = to
      end
      tokens[i] = out << text[cursor..]
    end
    tokens.join
  end
end

unless ENV["PSYCHOTRONIC_NO_AUTOLINK"] == "1"
  Jekyll::Hooks.register :site, :pre_render do |site|
    site.config["psychotronic_link_targets"] = PsychotronicReviewLinks.targets(site)
  end

  Jekyll::Hooks.register :posts, :post_convert do |post|
    targets = post.site.config["psychotronic_link_targets"]
    next unless targets
    post.content = PsychotronicReviewLinks.link(post.content, post.url, targets, post.site.baseurl.to_s)
  end
end
